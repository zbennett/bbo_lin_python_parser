from deal import Card, PlayerHand
from deal_enums import Suit, Direction
from play_utils import clear_rubber_points, get_rubber_points, calculate_vul, calculate_rubber_points, print_current_rubber_score, new_rubber, get_total_rubber_score
from lin import parse_single_lin, parse_multi_lin
from board_record import Contract
import math
import sys
import argparse

rubber_inc = 1
game_inc = 1
total_games = 0
rubbers = 0

parser = argparse.ArgumentParser()
parser.add_argument('file_name', type=str)
parser.add_argument('--rubbers', nargs='+')
parser.add_argument('--single', action='store_true')
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

file_name = args.file_name
rubber_list = args.rubbers
single =args.single
debug = args.debug
if args.rubbers == None :
    rubber_list = []

if(single) :
    thing = parse_single_lin(file_name)
else:
    thing = parse_multi_lin(file_name)



ns_points = 0
ew_points = 0

ns_points_rubber = 0
ew_points_rubber = 0

e_points = 0
w_points = 0
s_points = 0
n_points = 0

e_points_rubber = 0
w_points_rubber = 0
s_points_rubber = 0
n_points_rubber = 0

n_played = 0
e_played = 0
w_played = 0
s_played = 0

n_played_rubber = 0
e_played_rubber = 0
w_played_rubber = 0
s_played_rubber = 0

n_made = 0
e_made = 0
w_made = 0
s_made = 0

n_made_rubber = 0
e_made_rubber = 0
w_made_rubber = 0
s_made_rubber = 0

n_opening_hands = 0
s_opening_hands = 0
e_opening_hands = 0
w_opening_hands = 0

ns_total_rubber_points = 0
ew_total_rubber_points = 0

def weird_division(n, d):
    return round((n / d) * 100, 2) if d else 0

def clear_rubber():
    global rubber_inc
    global game_inc
    global total_games
    global rubber_list
    global n_points_rubber
    global s_points_rubber
    global e_points_rubber
    global w_points_rubber
    global n_points
    global s_points
    global e_points
    global w_points

    global n_played
    global e_played
    global w_played
    global s_played

    global n_played_rubber
    global e_played_rubber
    global w_played_rubber
    global s_played_rubber

    global n_made
    global e_made
    global w_made
    global s_made

    global n_made_rubber
    global e_made_rubber
    global w_made_rubber
    global s_made_rubber

    global ns_points
    global ew_points

    global ns_points_rubber
    global ew_points_rubber

    global ns_total_rubber_points
    global ew_total_rubber_points

    n_points += n_points_rubber
    s_points += s_points_rubber
    e_points += e_points_rubber
    w_points += w_points_rubber

    n_played += n_played_rubber
    s_played += s_played_rubber
    e_played += e_played_rubber
    w_played += w_played_rubber

    n_made += n_made_rubber
    s_made += s_made_rubber
    e_made += e_made_rubber
    w_made += w_made_rubber

    ns_points += ns_points_rubber
    ew_points += ew_points_rubber

    total_games += game_inc
    game_inc = 0
    rubber_inc += 1
    if len(rubber_list) > 0 :
        rubber_list.pop(0)
    n_points_rubber = 0
    s_points_rubber = 0
    e_points_rubber = 0
    w_points_rubber = 0

    n_played_rubber = 0
    s_played_rubber = 0
    e_played_rubber = 0
    w_played_rubber = 0

    n_made_rubber = 0
    s_made_rubber = 0
    e_made_rubber = 0
    w_made_rubber = 0

    ns_points_rubber = 0
    ew_points_rubber = 0

    rub_points = get_rubber_points()
    if rub_points[0] + rub_points[1] != 0 :
        print("*",bRecords.names.get(Direction.NORTH), "/", bRecords.names.get(Direction.SOUTH), "Rubber Score:", rub_points[0],"*")
        print("*",bRecords.names.get(Direction.EAST), "/", bRecords.names.get(Direction.WEST), "Rubber Score:", rub_points[1],"*")
    
    clear_rubber_points()

def print_points(rubber):
    global n_points_rubber
    global s_points_rubber
    global e_points_rubber
    global w_points_rubber

    global n_played_rubber
    global s_played_rubber
    global e_played_rubber
    global w_played_rubber

    global n_made_rubber
    global s_made_rubber
    global e_made_rubber
    global w_made_rubber

    global ns_points_rubber
    global ew_points_rubber

    print_str = "Rubber " + rubber + " (" + str(game_inc) + " games)"
    total_points = n_points_rubber + s_points_rubber + e_points_rubber + w_points_rubber
    if rubber == "final":
        if game_inc > 1 :
            print("--------------------------------------------------------")
            print_str2 = "Current Rubber" + "(" + str(game_inc-1) + " games)"
            print("          ***", print_str2, "***          ")
            print_current_rubber_score()
        clear_rubber()
        print_str = "Total" + " (" + str(total_games - 1) + " games)"
        total_points = n_points + s_points + e_points + w_points
        n_points_rubber = n_points
        s_points_rubber = s_points
        e_points_rubber = e_points
        w_points_rubber = w_points

        n_played_rubber = n_played
        s_played_rubber = s_played
        e_played_rubber = e_played
        w_played_rubber = w_played

        n_made_rubber = n_made
        s_made_rubber = s_made
        e_made_rubber = e_made
        w_made_rubber = w_made

        ns_points_rubber = ns_points
        ew_points_rubber = ew_points
    
    print("--------------------------------------------------------")
    # print()
    print("          ***", print_str, "***          ")
    print(bRecords.names.get(Direction.NORTH), "Points:", n_points_rubber, "(", weird_division(n_points_rubber, total_points),"%)",bRecords.names.get(Direction.SOUTH), "Points:", s_points_rubber, "(", weird_division(s_points_rubber, total_points),"%)")
    # print(bRecords.names.get(Direction.SOUTH), "Points:", s_points_rubber, "(", weird_division(s_points_rubber, total_points),"%)")
    print(bRecords.names.get(Direction.EAST), "Points:", e_points_rubber, "(", weird_division(e_points_rubber, total_points),"%)",bRecords.names.get(Direction.WEST), "Points:", w_points_rubber, "(", weird_division(w_points_rubber, total_points),"%)")
    # print(bRecords.names.get(Direction.WEST), "Points:", w_points_rubber, "(", weird_division(w_points_rubber, total_points),"%)")
    print()
    # print(bRecords.names.get(Direction.NORTH), "Opening hands:", n_opening_hands)
    # print(bRecords.names.get(Direction.SOUTH), "Opening hands:", s_opening_hands)
    # print(bRecords.names.get(Direction.EAST), "Opening hands:", e_opening_hands)
    # print(bRecords.names.get(Direction.WEST), "Opening hands:", w_opening_hands)
    # print()
    if rubber == "final":
        print(bRecords.names.get(Direction.NORTH), "Played:", n_played_rubber, "and made:", n_made_rubber, "(", weird_division(n_made_rubber, n_played_rubber),"%)")
        print(bRecords.names.get(Direction.SOUTH), "Played:", s_played_rubber, "and made:", s_made_rubber, "(", weird_division(s_made_rubber,s_played_rubber),"%)")
        print(bRecords.names.get(Direction.EAST), "Played:", e_played_rubber, "and made:", e_made_rubber, "(", weird_division(e_made_rubber,e_played_rubber),"%)")
        print(bRecords.names.get(Direction.WEST), "Played:", w_played_rubber, "and made:", w_made_rubber, "(", weird_division(w_made_rubber,w_played_rubber),"%)")
        print()
        # print(bRecords.names.get(Direction.NORTH), "Opening Hands:", n_opening_hands)
        # print(bRecords.names.get(Direction.SOUTH), "Opening Hands:", s_opening_hands)
        # print(bRecords.names.get(Direction.EAST), "Opening Hands:", e_opening_hands)
        # print(bRecords.names.get(Direction.WEST), "Opening Hands:", w_opening_hands)
        # print()
    print(bRecords.names.get(Direction.NORTH), "/", bRecords.names.get(Direction.SOUTH), "Points:", ns_points_rubber, "(", weird_division(ns_points_rubber, ns_points_rubber + ew_points_rubber),"%)")
    print(bRecords.names.get(Direction.EAST), "/", bRecords.names.get(Direction.WEST), "Points:", ew_points_rubber, "(", weird_division(ew_points_rubber, ns_points_rubber + ew_points_rubber),"%)")
    print()
    if rubber == "final":
        tot_rub = get_total_rubber_score()
        print("*",bRecords.names.get(Direction.NORTH), "/", bRecords.names.get(Direction.SOUTH), "Total Rubber Score:", tot_rub[0],"*")
        print("*",bRecords.names.get(Direction.EAST), "/", bRecords.names.get(Direction.WEST), "Total Rubber Score:", tot_rub[1],"*")



# print(thing)
for dealio in thing:
    for bRecords in dealio.board_records:
        # print("names: ", bRecords.names)
        # print("Cards: ", dealio.deal.player_cards)
        # print(bRecords.names.get(Direction.NORTH), dealio.deal.hands.get(Direction.NORTH).getPoints())
        # print(bRecords.names.get(Direction.SOUTH), dealio.deal.hands.get(Direction.SOUTH).getPoints())
        # print(bRecords.names.get(Direction.EAST), dealio.deal.hands.get(Direction.EAST).getPoints())
        # print(bRecords.names.get(Direction.WEST), dealio.deal.hands.get(Direction.WEST).getPoints())
        # print("Bidder: ", bRecords.names.get(bRecords.declarer))
        # print("contract: ", bRecords.contract)
        # print("Tricks won:", bRecords.tricks)
        # print("score: ", bRecords.score)
        # print("ns_vul", dealio.deal.ns_vulnerable)
        # print("ew_vul", dealio.deal.ew_vulnerable)
        # print(bRecords.)
        ns_points_rubber += dealio.deal.hands.get(Direction.NORTH).getPoints()
        ns_points_rubber += dealio.deal.hands.get(Direction.SOUTH).getPoints()
        ew_points_rubber += dealio.deal.hands.get(Direction.EAST).getPoints()
        ew_points_rubber += dealio.deal.hands.get(Direction.WEST).getPoints()
        n_points_rubber += dealio.deal.hands.get(Direction.NORTH).getPoints()
        s_points_rubber += dealio.deal.hands.get(Direction.SOUTH).getPoints()
        e_points_rubber += dealio.deal.hands.get(Direction.EAST).getPoints()
        w_points_rubber += dealio.deal.hands.get(Direction.WEST).getPoints()

        calculate_vul(bRecords.declarer, bRecords.zach_score)
        # honors = dealio.deal.hands.get(bRecords.declarer).getHonors(bRecords.contract.suit)
        # if honors != 0 :
        #     print("HONORS:",honors)
        #     print("Bidder: ", bRecords.names.get(bRecords.declarer))
        #     print("contract: ", bRecords.contract)
        #     print("Tricks won:", bRecords.tricks)
        calculate_rubber_points(bRecords.contract.level, bRecords.contract.suit, bRecords.contract.doubled, bRecords.tricks, bRecords.declarer, dealio.deal.hands.get(bRecords.declarer).getHonors(bRecords.contract.suit), debug)

        if dealio.deal.hands.get(Direction.NORTH).getPoints() > 12 :
            n_opening_hands += 1
        elif dealio.deal.hands.get(Direction.SOUTH).getPoints() > 12 :
            s_opening_hands += 1
        elif dealio.deal.hands.get(Direction.EAST).getPoints() > 12 :
            e_opening_hands += 1
        elif dealio.deal.hands.get(Direction.WEST).getPoints() > 12 :
            w_opening_hands += 1

        if bRecords.declarer == Direction.NORTH:
            n_played_rubber  += 1
            if (bRecords.tricks - 6 ) >= bRecords.contract.level:
                n_made_rubber  += 1
        elif bRecords.declarer == Direction.SOUTH:
            s_played_rubber  +=1
            if (bRecords.tricks - 6 ) >= bRecords.contract.level:
                s_made_rubber  += 1
        elif bRecords.declarer == Direction.EAST:
            e_played_rubber  +=1
            if (bRecords.tricks - 6 ) >= bRecords.contract.level:
                e_made_rubber  += 1
        elif bRecords.declarer == Direction.WEST:
            w_played_rubber  +=1
            if (bRecords.tricks - 6 ) >= bRecords.contract.level:
                w_made_rubber += 1
        if new_rubber() :
            print_points(str(rubber_inc))
            clear_rubber()
        game_inc += 1
                
print_points("final")





