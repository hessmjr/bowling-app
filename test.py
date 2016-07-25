from unittest import TestCase, main
from mongoengine import connect
import json

from api import app
from datastore import Game, Player


class TestHomeEndpoint(TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_valid_status(self):
        """
        Tests for valid status
        """
        response = self.app.get('/')
        data = response.data
        assert "Start bowling!" in data

    def test_invalid_route(self):
        """
        Tests for invalid path requested
        """
        response = self.app.get('/nothere')
        assert '404' in response.status

    def test_invalid_method(self):
        """
        Tests for invalid methods used
        """
        players = [
            "Calvin Johnson",
            "Michael Jordan"
        ]
        response = self.app.post('/', data=json.dumps(players))
        assert '405' in response.status


class TestAllGamesEndpoint(TestCase):

    def setUp(self):
        """
        Setup app and database before test suite
        """
        self.app = app.test_client()
        db = connect("bowlingdb")
        db.drop_database("bowlingdb")

    def test_get_all_games(self):
        """
        Tests retrieving all games
        """
        # add a game to database
        new_players = [
            "Calvin Johnson",
            "Michael Jordan"
        ]
        players = []
        for num, name in enumerate(new_players):
            players.append(Player(player_id=(num + 1), name=name))
        game = Game(players=players)
        game.save()

        # query api for list of games
        response = self.app.get('/games')
        assert '200' in response.status
        data = json.loads(response.data)
        assert list == type(data)
        assert 1 == len(data)

    def test_create_valid_game(self):
        """
        Tests posting a valid game
        """
        players = [
            "Calvin Johnson",
            "Michael Jordan"
        ]
        response = self.app.post('/games', data=json.dumps(players))
        assert '201' in response.status
        data = json.loads(response.data)
        assert "gameID" in data

    def test_create_invalid_game(self):
        """
        Test creating invalid games
        """
        # Test for 0 players
        no_players = []
        response = self.app.post('/games', data=json.dumps(no_players))
        assert '400' in response.status

        # test for more than 5 players
        many = [
            "Calvin Johnson",
            "Michael Jordan",
            "Jarret Jack",
            "Chris Bosh",
            "D Thomas"
        ]
        response = self.app.post('/games', data=json.dumps(many))
        assert '400' in response.status

        # test for invalid json
        invalid = "Calvin Johnson"
        response = self.app.post('/games', data=json.dumps(invalid))
        assert '400' in response.status

    def test_invalid_method(self):
        """
        Tests for invalid methods used
        """
        players = [
            "Calvin Johnson",
            "Michael Jordan"
        ]
        response = self.app.put('/games', data=json.dumps(players))
        assert '405' in response.status


class TestGamesEndpoint(TestCase):

    def setUp(self):
        """
        Setup app, database, and create a game before test cases
        """
        self.app = app.test_client()
        db = connect("bowlingdb")
        db.drop_database("bowlingdb")

        # add a game
        new_players = [
            "Calvin Johnson",
            "Michael Jordan"
        ]
        players = []
        for num, name in enumerate(new_players):
            players.append(Player(player_id=(num + 1), name=name))
        game = Game(players=players)
        game_info = game.save()
        self.valid_id = str(game_info.id)

    def test_getting_game(self):
        """
        Tests requesting valid and invalid games
        """
        # request with an invalid id
        bad_id = "badid"
        response = self.app.get('/games/' + bad_id)
        assert '400' in response.status

        # request with an id not matching
        not_found_id = "5795434f0640fd14497c3888"
        response = self.app.get('/games/' + not_found_id)
        assert '404' in response.status

        # request with a valid id
        response = self.app.get('/games/' + self.valid_id)
        assert '200' in response.status
        assert self.valid_id in response.data

    def test_sending_scores(self):
        """
        Tests sending new scores to the game
        """
        # send an invalid body
        response = self.app.put('/games/' + self.valid_id, data='hi')
        assert '400' in response.status

        # send an invalid bowl
        response = self.app.put('/games/' + self.valid_id, data='12')
        assert '400' in response.status

        # send a valid bowl
        response = self.app.put('/games/' + self.valid_id, data='10')
        assert '200' in response.status

        # test send score and game not active
        self.app.delete('/games/' + self.valid_id)
        response = self.app.put('/games/' + self.valid_id, data='10')
        assert '400' in response.status

    def test_delete_game(self):
        """
        Tests inactiving games
        """
        # Delete invalid player
        response = self.app.delete('/games/' + self.valid_id, data='hi')
        assert '400' in response.status
        response = self.app.delete('/games/' + self.valid_id, data='6')
        assert '400' in response.status

        # Delete valid player
        response = self.app.delete('/games/' + self.valid_id, data='1')
        assert '200' in response.status

        # Delete inactive player
        response = self.app.delete('/games/' + self.valid_id, data='1')
        assert '400' in response.status

        # Delete an invalid game
        response = self.app.delete('/games/5795434f0640fd14497c3888')
        assert '404' in response.status

        # Delete a valid game
        response = self.app.delete('/games/' + self.valid_id)
        assert '200' in response.status
        assert self.valid_id in response.data

        # Delete an inactive game
        response = self.app.delete('/games/' + self.valid_id)
        assert '400' in response.status

    def test_invalid_method(self):
        """
        Tests for invalid methods used
        """
        players = [
            "Calvin Johnson",
            "Michael Jordan"
        ]
        response = self.app.post('/games/5795434f0640fd14497c3888',
                                 data=json.dumps(players))
        assert '405' in response.status


class TestScoring(TestCase):

    def test_score_calculation(self):
        """
        Tests scoresheet method
        """
        # test 3 strikes
        scores = [10, 0, 10, 0, 10, 0]
        info = Player.calc_score_sheet(scores)
        assert info["frame_results"][-1] == 'X'
        assert info["total"] == 60

        # test all strikes
        scores = [10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 10, 0,
                  10, 0, 10, 0, 10, 0, 10, 10, 10]
        info = Player.calc_score_sheet(scores)
        assert info['frame_scores'][-1] == 30
        assert info["total"] == 300

        # test all spares
        scores = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                  5, 5, 5, 5, 5, 5, 10]
        info = Player.calc_score_sheet(scores)
        assert info["frame_results"][-1] == '5-5-X'
        assert info["total"] == 155

        # test various scores
        scores = [3, 4, 10, 0, 5, 5, 10, 0]
        info = Player.calc_score_sheet(scores)
        assert info["frame_scores"][1] == 20
        assert info["total"] == 57

if __name__ == '__main__':
    main()
