import botc.core.backend as backend
from botc.core.storyteller import storyteller
from botc.core.grimoire import grimoire


# 夜晚唤醒顺序：投毒者＞恶魔＞洗衣妇＞图书管理员＞调查员＞厨师＞共情者＞占卜师＞管家＞间谍，若场上无该角色，可直接顺延
First_Night_Order_List = ["投毒者", "小恶魔", "洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "管家", "间谍"]
Other_Nights_Order_List = ["投毒者", "僧侣", "小恶魔", "养鸦人", "共情者", "占卜师", "管家", "掘墓人", "间谍", "猩红女郎"]


def nights():
    for current_role in Other_Nights_Order_List:
        # 从[夜晚唤醒顺序]中获得当前使用技能的角色
        for player in grimoire.alive_list:
            # 仅当角色出现在此局游戏中时才能使用技能
            if player.true_role == current_role:
                player.skill()
                storyteller.check_kill_in_night()
