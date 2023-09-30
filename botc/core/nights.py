import botc.core.backend as backend
from botc.core.storyteller import storyteller
from botc.core.roles import bad_guys_list


# 夜晚唤醒顺序：投毒者＞恶魔＞洗衣妇＞图书管理员＞调查员＞厨师＞共情者＞占卜师＞管家＞间谍，若场上无该角色，可直接顺延
First_Night_Order_List = ["投毒者", "小恶魔", "洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "管家", "间谍"]
Other_Nights_Order_List = ["投毒者", "小恶魔", "共情者", "占卜师", "管家", "间谍", "掘墓人"]


def first_night(players_list):
    backend.info.append("游戏开始")
    alive_list = [i for i in players_list if i.is_alive]
    for player in alive_list:
        if player.is_bad_guy:
            # 满足人数条件时，坏人阵营提前获得信息
            player.passive_skill_before_game()
    backend.info.append("第1晚")
    for current_role in First_Night_Order_List:
        # 从[夜晚唤醒顺序]中获得当前使用技能的角色
        for player in alive_list:
            # 仅当角色出现在此局游戏中时才能使用技能
            if player.true_role == current_role and current_role != "小恶魔":
                player.passive_skill_first_night()
                player.passive_skill_every_night()
                player.skill_first_night()
                player.skill_every_night()
    storyteller.check_kill()
    backend.print_all_info()


def other_nights(players_list, nights_num):
    alive_list = [i for i in players_list if i.is_alive]
    backend.info.append(f"第{nights_num}晚")
    for current_role in Other_Nights_Order_List:
        # 从[夜晚唤醒顺序]中获得当前使用技能的角色
        for player in alive_list:
            # 仅当角色出现在此局游戏中时才能使用技能
            if player.true_role == current_role:
                player.passive_skill_other_nights()
                player.passive_skill_every_night()
                player.skill_other_nights()
                player.skill_every_night()
    storyteller.check_kill()
    backend.print_all_info()
