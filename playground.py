import random
import botc
from random import choice
import botc.core.roles as roles

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
    nights_num = 0
    while not good_guys_win and not bad_guys_win:
        if is_night:
            nights_num += 1
            is_night = False
            print("---------------------------------------------------------------------------------------------")
            print("现在是晚上")
            print("目前还存活的玩家编号为：", [i.player_index for i in players_list if i.is_alive])
            if is_first_night:
                is_first_night = False
                first_night(players_list)
            else:
                other_nights(players_list, nights_num)
        else:
            is_night = True
            print("---------------------------------------------------------------------------------------------")
            print("现在是白天")
            print("目前还存活的玩家编号为：", [i.player_index for i in players_list if i.is_alive])
            storyteller.vote_to_execute()


main(players_num)
