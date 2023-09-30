import botc.core.backend as backend
from botc.core.storyteller import storyteller


# 夜晚唤醒顺序：投毒者＞恶魔＞洗衣妇＞图书管理员＞调查员＞厨师＞共情者＞占卜师＞管家＞间谍，若场上无该角色，可直接顺延
First_Night_Order_List = ["投毒者", "小恶魔", "洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "管家", "间谍"]
Other_Nights_Order_List = ["投毒者", "小恶魔", "共情者", "占卜师", "管家", "间谍"]


def first_night(players_list):
    # 从[夜晚唤醒顺序]中获得当前使用技能的角色
    for current_role in First_Night_Order_List:
        # 仅当角色出现在此局游戏中时才能使用技能
        for player in players_list:
            if player.true_role == current_role and current_role != "小恶魔":
                player.passive_skill()
                player.skill()
    storyteller()
    backend.print_all_info()


def other_nights(players_list):
    # 从[夜晚唤醒顺序]中获得当前使用技能的角色
    for current_role in Other_Nights_Order_List:
        # 仅当角色出现在此局游戏中时才能使用技能
        for player in players_list:
            if player.true_role == current_role:
                player.passive_skill()
                player.skill()
    storyteller()
    backend.print_all_info()
