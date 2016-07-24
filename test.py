import unittest
import api
import json


class TestHomeEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = api.app.test_client()

    def test_valid_status(self):
        """
        Tests for valid status
        """
        response = self.app.get('/')
        data = json.loads(response.data)
        assert "Start bowling!" == data["message"]

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


class TestAllGamesEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = api.app.test_client()

    def test_get_all_games(self):
        """
        Tests retrieving all games
        """
        response = self.app.get('/games')
        # TODO seed with couple games

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
        response = self.app.put('/', data=json.dumps(players))
        assert '405' in response.status


# class TestGamesEndpoint(unittest.TestCase):
#
#     def test_get_invalid_game(self):
#         """
#         Tests requestings an invalid game
#         """
#
#     def test_get_valid_game(self):
#         """
#         Tests getting a valid game
#         """
#
#     # test send score and game not active
#     # test send score and player not active
#     # test send score and not player turn
#     # test send two valid scores
#     # test send two scores and only one needed
#     # test send a strike and has strikes
#     # test send a spare and has strikes
#     # test first frame
#     # test final frame
#
#     def test_delete_active_player(self):
#         """
#         Tests inactivating active player
#         """
#
#     def test_delete_inactive_player(self):
#         """
#         Tests trying to inactivate inactive player
#         """

if __name__ == '__main__':
    unittest.main()
