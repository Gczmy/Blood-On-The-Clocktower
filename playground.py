import random
import botc
from random import choice
import botc.core.roles as roles
import botc.core.daytime as daytime

from botc.core.players import create_players_list
from botc.core.nights import first_night
from botc.core.nights import other_nights
from botc.core.storyteller import storyteller

players_num = 8


def main(players_num):
    print("游戏开始")
    players_list = create_players_list(players_num)
    print([i.true_role for i in players_list])
    storyteller.players_list = players_list
    if players_num >= 7:
        print("七人或七人以上的局，爪牙与恶魔互相认识但是不知道对方具体身份 ，且恶魔知道三个不在场的好人身份")

    good_guys_win = False
    bad_guys_win = False
    is_first_night = True
    is_night = True
    while not good_guys_win and not bad_guys_win:
        if is_night:
            is_night = False
            print("---------------------------------------------------------------------------------------------")
            print("现在是晚上")
            alive_list = daytime.check_alive(players_list)
            if is_first_night:
                is_first_night = False
                first_night(alive_list)
            else:
                other_nights(alive_list)
        else:
            is_night = True
            print("---------------------------------------------------------------------------------------------")
            print("现在是白天")
            alive_list = daytime.check_alive(players_list)
            execute_player = storyteller.vote_to_execute()


main(players_num)
