import botc.core.backend as backend
from botc.core.storyteller import storyteller
from botc.core.roles import bad_guys_list


# 夜晚唤醒顺序：投毒者＞恶魔＞洗衣妇＞图书管理员＞调查员＞厨师＞共情者＞占卜师＞管家＞间谍，若场上无该角色，可直接顺延
First_Night_Order_List = ["投毒者", "小恶魔", "洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "管家", "间谍"]
Other_Nights_Order_List = ["投毒者", "僧侣", "小恶魔", "养鸦人", "共情者", "占卜师", "管家", "掘墓人", "间谍", "猩红女郎"]


def first_night(players_list, alive_list):
    backend.info.append("游戏开始")
    for player in alive_list:
        if player.is_bad_guy:
            # 满足人数条件时，坏人阵营提前获得信息
            player.passive_skill_before_game()
    backend.info.append("第1个夜晚")
    for current_role in First_Night_Order_List:
        # 从[夜晚唤醒顺序]中获得当前使用技能的角色
        for player in alive_list:
            # 仅当角色出现在此局游戏中时才能使用技能
            if player.true_role == current_role:
                player.passive_skill_first_night()
                player.passive_skill_every_night(alive_list)
                player.skill_first_night()
                player.skill_every_night(alive_list)
                storyteller.check_kill_in_night()
    backend.print_all_info()


def other_nights(players_list, alive_list, nights_num):
    backend.info.append(f"第{nights_num}个夜晚")
    for current_role in Other_Nights_Order_List:
        # 从[夜晚唤醒顺序]中获得当前使用技能的角色
        for player in alive_list:
            # 仅当角色出现在此局游戏中时才能使用技能
            if player.true_role == current_role:
                player.passive_skill_other_nights(alive_list)
                player.passive_skill_every_night(alive_list)
                player.skill_other_nights(alive_list)
                player.skill_every_night(alive_list)
                storyteller.check_kill_in_night()
    backend.print_all_info()
