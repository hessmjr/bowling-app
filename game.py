from mongoengine import *

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
    #gameID = ObjectIdField(primary_key=True)
    players = ListField(EmbeddedDocumentField(Player), min_length=1,
                        max_length=4, required=True)
    meta = {'collection': 'games'}

    @queryset_manager
    def games(self, queryset):
        """

        :param queryset:
        :return:
        """
        return queryset
