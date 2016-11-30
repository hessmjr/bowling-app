from mongoengine import *
from datetime import datetime

# Connects mongoDB to this database namespace
connect('bowlingdb')


class Player(EmbeddedDocument):
    """
    Object relational mapping for an individual player
    """
    player_id = IntField(min_value=1, max_value=4, required=True)
    name = StringField(min_length=1, required=True)
    active = BooleanField(default=True)
    raw_scores = ListField(IntField(min_value=0, max_value=10))

    STRIKE = "X"
    SPARE = "S"

    @classmethod
    def calc_score_sheet(cls, scores):
        """
        Calculates player's frame results, frame scores, and running totals
        """
        frame_results, frame_scores, running_totals = [], [], []

        # calculate frame results and frame scores
        for roll, score in enumerate(scores):
            frame = roll / 2

            # add in fill scores for last frame strike or spare
            if roll > 18 and (scores[18] == 10 or sum(scores[18:20]) == 10):
                # add extra score to last frame's strike
                frame_scores[9] += score

                # append correct result
                if score == 10:
                    frame_results[9] += "-" + str(cls.STRIKE)
                else:
                    frame_results[9] += "-" + str(score)
                continue

            # check if frame's first roll
            if roll % 2 != 1:
                frame_score = score

                # add strike symbol and strike score
                if score == 10:
                    frame_results.append(cls.STRIKE)

                    # add additional points
                    frame_score += cls.__add_extra(cls.STRIKE, roll, scores)
                else:
                    frame_results.append(str(score))

                # add new score entry to frame result
                frame_scores.append(frame_score)
                continue

            # assume frame's second roll and set frame final score
            frame_score = frame_scores[-1] + score

            # if score equals 10 and not a strike, then spare
            if score != 0 and frame_score == 10:
                # add spare to frame result
                frame_results[frame] += "-" + str(cls.SPARE)

                # get next roll
                frame_score += cls.__add_extra(cls.SPARE, roll, scores)

            # otherwise only use score if first wasn't a strike
            elif frame_score < 10:
                frame_results[frame] += "-" + str(score)

            # set new frame score
            frame_scores[-1] = frame_score

        # sum up frame scores for current total
        total = sum(frame_scores)

        # set all player score values
        scoresheet = {
            "frame_results": frame_results,
            "frame_scores": frame_scores,
            "total": total
        }
        return scoresheet

    @classmethod
    def __add_extra(cls, roll_type, roll_num, scores):
        """
        Grabs any extra points for scoring a strike or a spare

        :param roll_type: STRIKE or SPARE
        :param roll_num: current roll number
        :param scores: list of all scores
        :return: extra points integer
        """
        extra_points = 0

        # if type spare then get next roll
        if roll_type == cls.SPARE:
            if roll_num + 1 < len(scores) - 1:
                extra_points += scores[roll_num + 1]

        # if type strike get next two valid rolls
        if roll_type == cls.STRIKE:
            second_roll, third_roll = 0, 0

            # skip next roll since 0, grab 2nd
            if roll_num + 2 < len(scores) - 1:
                second_roll = scores[roll_num + 2]

            # grab 3rd roll unless 2nd was strike or fill
            if roll_num + 3 < len(scores) - 1 \
                    and (second_roll < 10 or roll_num + 3 == 19):
                third_roll = scores[roll_num + 3]

            # if 2nd roll was strike grab the 4th
            elif roll_num + 4 < len(scores) - 1:
                third_roll = scores[roll_num + 4]

            # sum the next two valid rolls to add to frame score
            extra_points = second_roll + third_roll

        return extra_points


class Game(Document):
    """
    Object relational mapping for main Game data structure
    """
    players = ListField(EmbeddedDocumentField(Player), min_length=1,
                        max_length=4, required=True)
    active = BooleanField(default=True)
    date_started = DateTimeField(default=datetime.now)
    meta = {'collection': 'games'}

    @queryset_manager
    def games(self, query_set):
        """
        Method that renames objects to games
        :param query_set: query paramaters
        :return: Game objects
        """
        return query_set
