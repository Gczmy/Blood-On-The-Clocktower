import botc.core.backend as backend
from botc.core.grimoire import grimoire
from botc.core.roles import player_input
from botc.core.players import create_players_list
from botc.core.nights import nights
from botc.core.storyteller import storyteller
from botc.core.ai import Prompt
from botc.core.print import print_to_all
from botc.core.print import print_to_role
from botc.core.print import clear_all_print_file
from botc.core.print import print_to_prompt
from botc.core.print import print_to_backend

grimoire.players_num = 8


def main():
    grimoire.players_list = create_players_list(grimoire.players_num)
    clear_all_print_file(grimoire.players_list)
    print_to_all("游戏开始")
    print_to_all(f"本局游戏的玩家角色为：{[i.true_role for i in grimoire.players_list]}")
    if grimoire.players_num >= 7:
        print_to_all("七人或七人以上的局，爪牙与恶魔互相认识但是不知道对方具体身份 ，且恶魔知道三个不在场的好人身份")
    good_guys_win = False
    bad_guys_win = False
    prompt = Prompt(grimoire.players_list)
    # print_to_prompt(prompt.prompt_initial)
    grimoire.before_game = False
    while not good_guys_win and not bad_guys_win:
        if grimoire.is_night:
            grimoire.nights_num += 1
            print_to_all("---------------------------------------------------------------------------------------------")
            print_to_all(f"现在是第{grimoire.nights_num}个夜晚")
            alive_list = [i for i in grimoire.players_list if i.is_alive]
            grimoire.alive_list = alive_list
            alive_index_list = [i.player_index for i in grimoire.alive_list]
            print_to_all(f"目前还存活的玩家编号为：{alive_index_list}")
            print_to_all(f"等待玩家进行夜晚技能操作")
            nights()
            print_to_all(f"玩家夜晚技能操作完成")
            for i in grimoire.players_list:
                print_to_role(i.true_role, i.info)
            if grimoire.is_first_night:
                grimoire.is_first_night = False
            grimoire.is_night = False
        else:
            print_to_all("---------------------------------------------------------------------------------------------")
            print_to_all(f"现在是第{grimoire.nights_num}个白天")

            storyteller.check_kill_in_daytime()
            alive_list = [i for i in grimoire.players_list if i.is_alive]
            grimoire.alive_list = alive_list
            print_to_all(f"目前还存活的玩家编号为：{[i.player_index for i in grimoire.alive_list]}")

            storyteller.check_daytime_skill()
            storyteller.nomination()
            grimoire.is_night = True
        good_guys_win, bad_guys_win = storyteller.check_win()
    if good_guys_win:
        print_to_all("游戏结束！恭喜好人阵营获得胜利！")
    if bad_guys_win:
        print_to_all("游戏结束！恭喜坏人阵营获得胜利！")


main()
