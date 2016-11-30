import json

from flask import Flask, Response, request
from flask_restful import Api, Resource
from mongoengine import DoesNotExist
from bson import ObjectId

from datastore import Game, Player

app = Flask(__name__)
api = Api(app)


################################
# Build API Resources
################################

class HomeRoute(Resource):

    def get(self):
        """
        GET method for home endpoint
        :return: Status of application
        """
        message = "------------------ Start bowling! ------------------\n\n" + \
                  "How to use api:\n\n" + \
                  "GET '/' \t\t\t\t\t=> Status and usage\n" + \
                  "GET '/games' \t\t\t\t=> List of all games\n" + \
                  "POST '/games \t\t\t\t=> Create a new game\n" + \
                  "GET '/games/{game_id}' \t\t=> " \
                  "Retrieve specific game info\n" + \
                  "PUT '/games/{game_id}' \t\t=> Send a bowl\n" + \
                  "DELETE '/games/{game_id}' \t=> Inactivate game or player"
        return Response(message, status=200)


class GamesRoute(Resource):

    def get(self):
        """
        GET method for querying all games
        :return: List of all games in database
        """
        all_games = []

        # grab essential info about each game
        try:
            for game in Game.games:
                players = []

                # build each game's information map
                game_info = {
                    "game_id": str(game.id),
                    "active": game.active
                }

                # get each player's name
                for player in game.players:
                    players.append(player.name)
                game_info["players"] = players

                all_games.append(game_info)

            # return list of all games
            return all_games

        # any processing errors notify user
        except Exception as exception:
            return server_issue(exception, error="GET AllGames")

    def post(self):
        """
        POST method for creating a new game
        :return: game id of newly created game
        """
        # try to parse the json request
        try:
            new_players = json.loads(request.data)
            print 'here'
            if not (0 < len(new_players) < 5):
                return bad_request("Invalid number of players")

            # build each new player
            players = []
            for num, name in enumerate(new_players):
                players.append(Player(player_id=(num + 1), name=name))
            print 'here2'
            # build a new game
            game = Game(players=players)
            new_game = game.save()
            game_id = str(new_game.id)
            print 'here3'
            # return newly created game ID to user
            message = {
                "gameID": game_id,
                "message": "New game created."
            }
            return Response(json.dumps(message), status=201,
                            mimetype='application/json')

        # any processing errors notify user
        except Exception as exception:
            return server_issue(exception, "POST AllGames")


class GameRoute(Resource):

    def get(self, game_id):
        """
        GET method for retrieving a single game's info
        :param game_id: id to query db on
        :return: full game information
        """
        try:
            # check if id valid and query for it
            check = self.__query_game_id(game_id)
            if type(check) != Game:
                return check
            else:
                game = check

            # build game info object
            game_info = {
                "id": str(game.id),
                "active": game.active,
                "date_started": str(game.date_started)
            }

            # build player info and scoresheet
            all_players = []
            for player in game.players:
                player_info = {
                    "player_id": player.player_id,
                    "name": player.name,
                    "active": player.active,
                    "scoresheet": Player.calc_score_sheet(player.raw_scores)
                }
                all_players.append(player_info)
            game_info["players"] = all_players

            # return game info to user
            return game_info

        # any processing errors notify user
        except Exception as exception:
            return server_issue(exception, "GET Games")

    def put(self, game_id):
        """
        PUT endpoint for sending a new bowling roll
        :param game_id: game to update with a score
        :return: GET endpoint
        """
        try:
            # check if game good
            check = self.__query_game_id(game_id)
            if type(check) != Game:
                return check
            else:
                game = check

            # check if game active
            if not game.active:
                return bad_request("Game is no longer active")

            # validate roll value
            score = int(request.data)
            if not (0 <= score <= 10):
                return bad_request("Roll must be integer between 0 - 10")

            # assign roll to next valid player
            max_scores_len = 22
            for player in game.players:

                # if player is inactive then skip
                if not player.active:
                    continue

                # check if player's next roll (players are sorted)
                if len(player.raw_scores) < max_scores_len:
                    max_scores_len = len(player.raw_scores)
                    player_id = player.player_id
                    scores = player.raw_scores

                if len(player.raw_scores) % 2 == 1:
                    break

            # check if second roll too high
            if len(scores) < 19 and len(scores) % 2 == 1 and scores[-1] + score > 10:
                return bad_request("Second roll is too high")

            # if roll is a 10 then add 0 too unless end frame
            if score == 10 and len(scores) < 18:
                scores += [score, 0]
            else:
                scores.append(score)

            # update raw scores for player
            game.players[player_id - 1].raw_scores = scores

            # check if player still active
            player_active = len(scores) < 20 \
                or (sum(scores[18:]) > 10 and len(scores) < 21)
            if not player_active:
                game.players[player_id - 1].active = False

            # check if game still active
            if len(game.players) == player_id and not player_active:
                game.active = False

            # save updates and return updates to user
            game.save()
            return self.get(game_id)

        # let user know of any internal error
        except Exception as exception:
            return server_issue(exception, "PUT Games")

    def delete(self, game_id):
        """
        DELETE endpoint for ending a game early
        :param game_id:
        :return:
        """
        game_active = False

        try:
            # check if id valid and query for it
            check = self.__query_game_id(game_id)
            if type(check) != Game:
                return check
            else:
                game = check

            # if game already inactive return bad request
            if not game.active:
                return bad_request("Game already inactive")

            # if not trying to inactive player inactivate game
            if request.data is None or len(request.data) < 1:
                game.update(active=False)
                return self.get(game_id)

            # parse player id to an int
            player_id = int(request.data)

            # check if valid player id
            if not (0 < player_id < len(game.players) + 1):
                return bad_request("Player ID outside integer range")

            # inactive player matching id unless already inactive
            for player in game.players:
                player_active = player.active

                # if player id matches and active then update
                if player.player_id == player_id and player_active:
                    player_active = False
                    game.players[player_id - 1].active = player_active

                # if player id matches then player already inactive
                elif player.player_id == player_id:
                    return bad_request("Player already inactive")

                # check if any active players remain
                if player_active:
                    game_active = True

            # update game status too
            game.active = game_active

            # save updates and return game info to user
            game.save()
            return self.get(game_id)

        # error parsing player id to an int
        except ValueError:
            return bad_request("Player ID not a valid integer")

        # let user know of any internal error
        except Exception as exception:
            return server_issue(exception, "DELETE Games")

    def __query_game_id(self, game_id):
        """
        Method that checks if game id is valid and queries for it
        :param game_id:
        :return:
        """
        try:
            # check if valid object id
            if len(game_id) != 24:
                return bad_request("Invalid game id")

            # try to query for game id and convert to python object
            game = Game.games.get(id=ObjectId(game_id))
            return game

        # if query throws non-existent error then inform user
        except DoesNotExist:
            return not_found("Game ID can not be found")


################################
# Add endpoints to API
################################

api.add_resource(HomeRoute, '/')
api.add_resource(GamesRoute, '/games')
api.add_resource(GameRoute, '/games/<game_id>')


################################
# Add custom error messages
################################

@app.errorhandler(400)
def bad_request(error=None):
    """
    Response if there is a bad request from user

    :param error: string message
    :return: 400 response
    """
    message = "Bad request: " + str(error)
    return Response(message, status=400)


@app.errorhandler(404)
def not_found(error=None):
    """
    Reponse if a resource is not found in database or in a route

    :param error: string message
    :return: 404 response
    """
    message = 'URL: ' + request.url
    if error:
        message += "\n" + str(error)
    return Response(message, status=404)


@app.errorhandler(500)
def server_issue(exception, error=None):
    """
    Response if there was an issue processing a request

    :param exception: exception causing issued
    :param error: string message
    :return:
    """
    # log error
    print "Error type: " + str(type(exception))
    print "Message: " + str(exception.message)

    # build response to user
    message = "Internal error processing request"
    if error:
        print error
    return Response(message, status=500)


################################
# Start app
################################

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0'
    )
