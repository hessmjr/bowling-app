from flask import Flask, Response, request
from flask_restful import Api, Resource
import json

from game import Game, Player

app = Flask(__name__)
api = Api(app)


################################
# Build API resources
################################

class Home(Resource):

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
                  "DELETE '/games/{game_id}' \t=> Finish game"
        return Response(message, status=200)


class AllGames(Resource):

    def get(self):
        """
        GET method for querying all games
        :return: List of all games in database
        """
        all_games = []

        # grab essential info about each game
        try:
            for game in Game.games:
                game_info = dict()
                players = []

                # get useful info from each game
                game_info["game_id"] = str(game.id)
                game_info["active"] = game.active

                # get each player's name
                for player in game.players:
                    players.append(player.name)
                game_info["players"] = players

                # return complete game listing
                all_games.append(game_info)

        # any processing errors notify user
        except Exception as error:
            print error.message
            return server_issue()

        # return list of all games
        return all_games

    def post(self):
        """
        POST method for creating a new game
        :return: game id of newly created game
        """
        # try to parse the json request
        try:
            new_players = json.loads(request.data)
            if not (0 < len(new_players) < 5):
                return bad_request("Invalid number of players")

            # build each new player
            players = []
            for num, name in enumerate(new_players):
                players.append(Player(playerID=(num + 1), name=name))

            # build a new game
            game = Game(players=players)
            new_game = game.save()
            game_id = str(new_game.id)

        # any processing errors notify user
        except Exception as error:
            print error.message
            return server_issue()

        # return newly created game ID to user
        message = {
            "gameID": game_id,
            "message": "New game created."
        }
        return Response(json.dumps(message), status=201,
                        mimetype='application/json')


class Games(Resource):

    def get(self, game_id):
        Game.games()

        return game_id

    def put(self, game_id):
        return "something"

    def delete(self, game_id):
        return "gone"


################################
# Add resources
################################

api.add_resource(Home, '/')
api.add_resource(AllGames, '/games')
api.add_resource(Games, '/games/<game_id>')


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
    message = 'URL: ' + request.url + "\n"
    if error:
        message += str(error)
    return Response(message, status=404)


@app.errorhandler(500)
def server_issue(error=None):
    """
    Response if there was an issue processing a request

    :param error: string message
    :return:
    """
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
