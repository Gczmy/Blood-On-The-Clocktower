import botc.core.backend as backend
from botc.core.players import create_players_list
from botc.core.nights import first_night
from botc.core.nights import other_nights
from botc.core.storyteller import storyteller
from botc.core.ai import Prompt
from botc.core.print import print_to_all
from botc.core.print import print_to_role
from botc.core.print import clear_all_print_file
from botc.core.print import print_to_prompt
from botc.core.print import print_to_backend


players_num = 8


def main(players_num):
    players_list = create_players_list(players_num)
    clear_all_print_file(players_list)
    print_to_all("游戏开始")
    print_to_backend(f"本局游戏的玩家角色为：{[i.true_role for i in players_list]}")
    storyteller.players_list = players_list
    if players_num >= 7:
        print_to_all("七人或七人以上的局，爪牙与恶魔互相认识但是不知道对方具体身份 ，且恶魔知道三个不在场的好人身份")
    good_guys_win = False
    bad_guys_win = False
    is_first_night = True
    is_night = True
    nights_num = 0
    prompt = Prompt(players_list)
    print_to_prompt(prompt.prompt_initial)
    while not good_guys_win and not bad_guys_win:
        if is_night:
            nights_num += 1
            is_night = False
            print_to_all("---------------------------------------------------------------------------------------------")
            print_to_all("现在是晚上")
            print_to_all(f"目前还存活的玩家编号为：{[i.player_index for i in players_list if i.is_alive]}")
            if is_first_night:
                is_first_night = False
                first_night(players_list)
                print(prompt.prompt_first_night)
            else:
                other_nights(players_list, nights_num)
            for i in players_list:
                print_to_role(i.true_role, i.info)
        else:
            is_night = True
            backend.info.append(f"第{nights_num}个白天")
            print_to_all("---------------------------------------------------------------------------------------------")
            print_to_all("现在是白天")
            print_to_all(f"目前还存活的玩家编号为：{[i.player_index for i in players_list if i.is_alive]}")
            storyteller.vote_to_execute()
        good_guys_win, bad_guys_win = storyteller.check_win()
    if good_guys_win:
        print_to_all("游戏结束！恭喜好人阵营获得胜利！")
    if bad_guys_win:
        print_to_all("游戏结束！恭喜坏人阵营获得胜利！")

main(players_num)
