from mongoengine import *
from datetime import datetime

connect('bowlingdb')

#
# class Scoresheet(EmbeddedDocument):
#     """
#
#     """
#     frame_results = ListField(StringField(), max_length=10)
#     frame_scores = ListField(IntField(min_value=0, max_value=30), max_length=10)
#     running_totals = ListField(IntField(min_value=0), max_length=10)


class Player(EmbeddedDocument):
    """

    """
    playerID = IntField(min_value=1, max_value=4, required=True)
    name = StringField(min_length=1, required=True)
    active = BooleanField(default=True)
    raw_scores = ListField(IntField(min_value=0, max_value=10))
    # scoresheet = DictField(EmbeddedDocumentField(Scoresheet))


class Game(Document):
    """

    """
    players = ListField(EmbeddedDocumentField(Player), min_length=1,
                        max_length=4, required=True)
    active = BooleanField(default=True)
    date_started = DateTimeField(default=datetime.now)
    meta = {'collection': 'games'}

    @queryset_manager
    def games(self, query_set):
        """

        :param query_set:
        :return:
        """
        return query_set
