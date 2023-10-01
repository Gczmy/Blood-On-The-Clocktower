import random
from random import sample
from random import choice
from botc.core.print import print_to_backend

info = []


def print_all_info():
    for i in info:
        print_to_backend(i)


def print_last_info():
    print(info[-1])


def build_players(players_num, roles_in_game):
    roles_in_game = roles_in_game.copy()

    players_info = {}  # 玩家信息字典: key:玩家代号, value:[0]玩家编号，[1]玩家自身身份，[2]玩家存活信息，
    # [3]玩家状态信息：健康，中毒，醉酒，[4~n]玩家使用技能得到的信息
    players = []  # 玩家代号
    for i in range(players_num):
        players.append("玩家" + str(i + 1))
        # 为玩家随机选择配置中的角色
        role = choice(roles_in_game)
        # role = roles_in_game[0]
        players_info[players[i]] = [i + 1, role, "存活", "健康"]
        roles_in_game.remove(role)
    return players, players_info