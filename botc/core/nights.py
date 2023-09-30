import botc.core.backend as backend
from botc.core.storyteller import storyteller
from botc.core.roles import bad_guys_list


# 夜晚唤醒顺序：投毒者＞恶魔＞洗衣妇＞图书管理员＞调查员＞厨师＞共情者＞占卜师＞管家＞间谍，若场上无该角色，可直接顺延
First_Night_Order_List = ["投毒者", "小恶魔", "洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "管家", "间谍"]
Other_Nights_Order_List = ["投毒者", "小恶魔", "共情者", "占卜师", "管家", "间谍", "掘墓人"]


def first_night(players_list):
    for player in bad_guys_list:
        # 满足人数条件时，坏人阵营提前获得信息
        player.passive_skill()

    for current_role in First_Night_Order_List:
        # 从[夜晚唤醒顺序]中获得当前使用技能的角色
        for player in players_list:
            # 仅当角色出现在此局游戏中时才能使用技能
            if player.true_role == current_role and current_role != "小恶魔":
                    player.passive_skill()
                    player.skill()
    storyteller.check_kill()
    backend.print_all_info()


def other_nights(players_list):
    for current_role in Other_Nights_Order_List:
        # 从[夜晚唤醒顺序]中获得当前使用技能的角色
        for player in players_list:
            # 仅当角色出现在此局游戏中时才能使用技能
            if player.true_role == current_role:
                player.passive_skill()
                player.skill()
    storyteller.check_kill()
    backend.print_all_info()
