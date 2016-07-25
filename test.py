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
        Setup before each test case
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
            players.append(Player(playerID=(num + 1), name=name))
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
        Set up before each test case
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
            players.append(Player(playerID=(num + 1), name=name))
        game = Game(players=players)
        game_info = game.save()
        self.valid_id = game_info.id

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
        response = self.app.get('/games/' + str(self.valid_id))
        assert '200' in response.status

    def test_sending_scores(self):
        """
        Tests sending new scores to the game
        """
        # test send score and game not active
        # test send score and player not active
        # test send score and not player turn
        # test send two valid scores
        # test send two scores and only one needed
        # test send a strike and has strikes
        # test send a spare and has strikes
        # test first frame
        # test final frame

    def test_delete_game(self):
        """
        Tests inactiving games
        """
        # Delete an invalid game

        # Delete a valid game

        # Delete an inactive game

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

if __name__ == '__main__':
    main()
