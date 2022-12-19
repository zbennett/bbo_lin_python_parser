from functools import partial
from typing import Callable, Optional

from deal import Card
from deal_enums import BiddingSuit, Suit, Direction


ns_vul = False
ew_vul = False
ns_leg = 0
ew_leg = 0
ns_rubber_points = 0
ew_rubber_points = 0
new_rubber = False

def _evaluate_card(trump_suit: BiddingSuit, suit_led: Suit, card: Card) -> int:
    """
    Score a card on its ability to win a trick given the trump suit and the suit that was led to the trick
    :return: the card's score
    """
    score = card.rank.value[0]
    if card.suit == trump_suit.to_suit():
        score += 100
    elif card.suit != suit_led:
        score -= 100
    return score


def trick_evaluator(trump_suit: BiddingSuit, suit_led: Suit) -> Callable:
    """
    :return: a partial which takes a Card as an argument and returns an ordering score within the context of a trick in
    progress
    """
    return partial(_evaluate_card, trump_suit, suit_led)


_FIRST_TRICK_VALUE = {
    BiddingSuit.NO_TRUMP: 40,
    BiddingSuit.SPADES: 30,
    BiddingSuit.HEARTS: 30,
    BiddingSuit.DIAMONDS: 20,
    BiddingSuit.CLUBS: 20,
}
_TRICK_VALUE = {
    BiddingSuit.NO_TRUMP: 30,
    BiddingSuit.SPADES: 30,
    BiddingSuit.HEARTS: 30,
    BiddingSuit.DIAMONDS: 20,
    BiddingSuit.CLUBS: 20,
}


def _calculate_bonus(
    level: int, suit: BiddingSuit, doubled: int, vulnerable: bool, contracted_trick_score: int, overtricks: int
) -> int:
    score = 0
    # Slam bonus
    if level == 7:
        score += 1500 if vulnerable else 1000
    elif level == 6:
        score += 750 if vulnerable else 500

    # # Game / part-score
    # if contracted_trick_score >= 100:
    #     score += 500 if vulnerable else 300
    # else:
    #     score += 50

    # Overtricks
    if doubled == 0:
        score += overtricks * _TRICK_VALUE[suit]
    elif doubled == 1:
        score += 50
        score += overtricks * (200 if vulnerable else 100)
    elif doubled == 2:
        score += 100
        score += overtricks * (400 if vulnerable else 200)
    return score


_FIRST_UNDERTRICK_VALUE = {
    (False, 0): 50,
    (False, 1): 100,
    (False, 2): 200,
    (True, 0): 100,
    (True, 1): 200,
    (True, 2): 400,
}

_SECOND_THIRD_UNDERTRICK_VALUE = {
    (False, 0): 50,
    (False, 1): 200,
    (False, 2): 400,
    (True, 0): 100,
    (True, 1): 300,
    (True, 2): 600,
}

_SUBSEQUENT_UNDERTRICK_VALUE = {
    (False, 0): 50,
    (False, 1): 300,
    (False, 2): 600,
    (True, 0): 100,
    (True, 1): 300,
    (True, 2): 600,
}

def new_rubber() -> bool:
    return new_rubber

def calculate_vul(declarer: Direction, points):
    global ns_leg
    global ns_vul
    global ew_leg
    global ew_vul
    global ns_rubber_points
    global ew_rubber_points
    global new_rubber

    new_rubber = False

    if declarer == Direction.NORTH or declarer == Direction.SOUTH:
        if points + ns_leg >= 100 :
            if ns_vul == True:
                if ew_vul == True:
                    ns_rubber_points += 500
                    new_rubber = True
                else:
                    ns_rubber_points += 700
                    new_rubber = True
                ns_vul = False
                ew_vul = False
            else:
                ns_vul = True
            ns_leg = 0
            ew_leg = 0
        else:
            ns_leg = points
    else:
        if points + ew_leg >= 100 :
            if ew_vul == True:
                if ns_vul == True:
                    ew_rubber_points += 500
                    new_rubber = True
                else:
                    ew_rubber_points += 700
                    new_rubber = True
                ew_vul = False
                ns_vul = False
            else:
                ew_vul = True
            ew_leg = 0
            ns_leg = 0
        else:
            ew_leg = points

    # print("Nort/South Vul:", ns_vul, "North/South Leg:", ns_leg)
    # print("East/West Vul:", ew_vul, "East/West Leg:", ew_leg)

def clear_rubber_points():
    global ew_rubber_points
    global ns_rubber_points

    ew_rubber_points = 0
    ns_rubber_points = 0

def print_rubber_points():
    print("____NS TOTAL RUBBER POINTS_____", ns_rubber_points)
    print("____EW TOTAL RUBBER POINTS_____", ew_rubber_points)

def print_current_rubber_score():
    print("N/S Leg:", ns_leg)
    print ("E/W Leg:", ew_leg)
    print("N/S Vul:", ns_vul)
    print("E/W Vul:", ew_vul)

def calculate_rubber_score(level: int, suit: Optional[BiddingSuit], doubled: int, tricks: int,  ) -> int:
    """
    :param level: contract level (4 in 4S)
    :param suit: contract bidding suit
    :param doubled: 0=undoubled, 1=doubled, 2=redoubled
    :param tricks: tricks taken by declarer
    :param vulnerable: vulnerability of declarer
    :return: declarer's score
    """
    if level == 0:  # Pass Out
        return 0
    scoring_tricks = tricks - 6
    if scoring_tricks >= level:
        double_multiplier = pow(2, doubled)
        first_trick_score = _FIRST_TRICK_VALUE[suit] * double_multiplier
        subsequent_tricks_score = _TRICK_VALUE[suit] * double_multiplier * (level - 1)
        # print("Game points:", first_trick_score + subsequent_tricks_score)
        return first_trick_score + subsequent_tricks_score 
    else:
        # print("Game points:", 0)
        return 0

def calculate_rubber_points(level: int, suit: Optional[BiddingSuit], doubled: int, tricks: int, declarer: Direction):
    """
    :param level: contract level (4 in 4S)
    :param suit: contract bidding suit
    :param doubled: 0=undoubled, 1=doubled, 2=redoubled
    :param tricks: tricks taken by declarer
    :param vulnerable: vulnerability of declarer
    :return: declarer's score
    """
    global ns_rubber_points
    global ew_rubber_points

    if declarer == Direction.NORTH or declarer == Direction.SOUTH:
        vulnerable = ns_vul
    else:
         vulnerable = ew_vul

    if level == 0:  # Pass Out
        return 0
    scoring_tricks = tricks - 6
    if scoring_tricks >= level:
        double_multiplier = pow(2, doubled)
        first_trick_score = _FIRST_TRICK_VALUE[suit] * double_multiplier
        subsequent_tricks_score = _TRICK_VALUE[suit] * double_multiplier * (level - 1)
        bonus = _calculate_bonus(
            level, suit, doubled, vulnerable, first_trick_score + subsequent_tricks_score, scoring_tricks - level
        )
        # print("Bonus:", bonus)
        points = first_trick_score + subsequent_tricks_score + bonus
    else:
        undertricks = level + 6 - tricks
        score_key = (vulnerable, doubled)
        score = 0
        for i in range(0, undertricks):
            score_dict = (
                _FIRST_UNDERTRICK_VALUE
                if i == 0
                else _SECOND_THIRD_UNDERTRICK_VALUE
                if 0 < i < 3
                else _SUBSEQUENT_UNDERTRICK_VALUE
            )
            score -= score_dict[score_key]
        points = score

    if declarer == Direction.NORTH or declarer == Direction.SOUTH:
        if points < 0 :
            ew_rubber_points += abs(points) 
        else:
            ns_rubber_points += points
    else:
        if points < 0 :
            ns_rubber_points += abs(points) 
        else:
            ew_rubber_points += points

    # print("North/South Rubber Points:", ns_rubber_points)
    # print("East/West Rubber Points:", ew_rubber_points)

def calculate_score(level: int, suit: Optional[BiddingSuit], doubled: int, tricks: int, vulnerable: bool) -> int:
    """
    :param level: contract level (4 in 4S)
    :param suit: contract bidding suit
    :param doubled: 0=undoubled, 1=doubled, 2=redoubled
    :param tricks: tricks taken by declarer
    :param vulnerable: vulnerability of declarer
    :return: declarer's score
    """
    if level == 0:  # Pass Out
        return 0
    scoring_tricks = tricks - 6
    if scoring_tricks >= level:
        double_multiplier = pow(2, doubled)
        first_trick_score = _FIRST_TRICK_VALUE[suit] * double_multiplier
        subsequent_tricks_score = _TRICK_VALUE[suit] * double_multiplier * (level - 1)
        bonus = _calculate_bonus(
            level, suit, doubled, vulnerable, first_trick_score + subsequent_tricks_score, scoring_tricks - level
        )
        return first_trick_score + subsequent_tricks_score + bonus
    else:
        undertricks = level + 6 - tricks
        score_key = (vulnerable, doubled)
        score = 0
        for i in range(0, undertricks):
            score_dict = (
                _FIRST_UNDERTRICK_VALUE
                if i == 0
                else _SECOND_THIRD_UNDERTRICK_VALUE
                if 0 < i < 3
                else _SUBSEQUENT_UNDERTRICK_VALUE
            )
            score -= score_dict[score_key]
        return score