from random import sample
from random import choice

# 玩家人数
players_num = 8
# 村民角色
# 洗衣妇 WasherWoman, 图书管理员 librarian, 调查员 investigator, 厨师 cook, 共情者 Empathiser, 占卜师 Soothsayer, 送葬者 mourner,
# 僧侣 monk, 养鸦人 crow raiser, 处女 virgin, 杀手 killer, 军人 soldier, 镇长 mayor
Villagers = ["洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "送葬者", "僧侣",
             "养鸦人", "处女", "杀手", "军人", "镇长"]
# 外来人角色
# 管家 Butler , 酒鬼 Drunkard, 隐士 Hermit, 圣人 Saint
Outlanders = ["管家", "酒鬼", "隐士", "圣人"]
# 爪牙角色
# 投毒者 Poisoner, 间谍 Spy, 猩红女郎 Scarlet Woman, 男爵 Baron
Minions = ["投毒者", "间谍", "猩红女郎", "男爵"]
# 恶魔角色
# 小恶魔 Imp
Demon = ["小恶魔"]
# 好人阵营
Good_guys = Villagers + Outlanders
# 坏人阵营
Bad_guys = Minions + Demon
# 旅人角色
# 替罪羊 Scapegoats, 枪手 Gunmen, 乞丐 Beggars, 官员 Officials, 盗贼 Thieves
Traveller = ["替罪羊", "枪手", "乞丐", "官员", "盗贼"]
# 所有角色
roles_all = Villagers + Outlanders + Minions + Demon + Traveller
# 从角色列表中随机选择个数为[玩家人数]的角色(无重复)
roles_in_game = sample(roles_all, players_num)

first_night = True

def build_players(players_num, roles_in_game):
    players_info = {}  # 玩家信息字典: key:玩家代号, value:[0]玩家编号，[1]玩家自身身份，[2]玩家使用技能得到的信息
    players = []  # 玩家代号
    for i in range(players_num):
        players.append("Player" + str(i))
        # 为玩家随机选择配置中的角色
        role = choice(roles_in_game)
        players_info[players[i]] = [i + 1, role]
        roles_in_game.remove(role)
    return players, players_info


# 夜晚唤醒顺序：投毒者＞恶魔＞洗衣妇＞图书管理员＞调查员＞厨师＞共情者＞占卜师＞管家＞间谍，若场上无该角色，可直接顺延
Night_Order_List = ["投毒者", "小恶魔", "洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "管家", "间谍"]


def Storyteller(role, players, players_info):
    """
    说书人
    """
    if role == "洗衣妇":
        """
        在游戏开始时，说书人会告诉洗衣妇某2名玩家中存在某一特定村民身份牌，但不知道具体哪名玩家持有此身份牌。
        返回：list = [村民身份牌，身份角色，另一随机角色]
        """
        # 找出本局所有村民并在其中随机选择一个
        Villagers_in_game = []
        for i in players_info:
            if i in Villagers:
                Villagers_in_game.append(i)
        villager = choice(Villagers_in_game)
        villager_player = [k for k, v in players_info.items() if v == villager][0]
        # 再随机选择一个角色
        players.remove(villager_player)
        rand_player = choice(players)
        return [villager, villager_player, rand_player]

    if role == "图书管理员":
        """
        在游戏开始时，可得知某2名玩家中存在某一特定外乡人身份牌，但不知道具体哪名玩家持有此身份牌（或得知本局不存在外乡人）。
        返回：["本局游戏没有外乡人。"] 或者 [外乡人身份牌，身份角色，另一随机角色]
        """
        Outlanders_in_game = []
        # 找出本局所有外乡人
        for i in players_info:
            if i in Villagers:
                Outlanders_in_game.append(i)
        # 如果本局游戏没有外乡人
        if not Outlanders_in_game:
            return ["本局游戏没有外乡人。"]
        # 如果本局游戏有外乡人，则随机选择一个外乡人身份牌
        else:
            outlander = choice(Outlanders_in_game)
            outlander_player = [k for k, v in players_info.items() if v == outlander][0]
            # 再随机选择一个角色
            players.remove(outlander_player)
            rand_player = choice(players)
            return [outlander, outlander_player, rand_player]

    if role == "调查员":
        """
        在游戏开始时，可得知某2名玩家中存在某一特定爪牙身份牌，但不知道具体哪名玩家为此身份。
        返回：[爪牙身份牌，身份角色，另一随机角色]
        """
        Minions_in_game = []
        # 找出本局所有爪牙并在其中随机选择一个
        for i in players_info:
            if i in Villagers:
                Minions_in_game.append(i)
        minions = choice(Minions_in_game)
        minions_player = [k for k, v in players_info.items() if v == minions][0]
        # 再随机选择一个角色
        players.remove(minions_player)
        rand_player = choice(players)
        return [minions, minions_player, rand_player]

    if role == "厨师":
        """
        在游戏开始时，可得知有多少对邪恶阵营玩家座位相邻。
        返回：[有{x}对邪恶阵营玩家座位相邻。]
        """
        Bad_guys_in_game = []
        # 找出本局所有邪恶阵营玩家
        for i in players_info:
            if i in Bad_guys:
                Bad_guys_in_game.append(i)
        bad_guys_player = [k for k, v in players_info.items() if v in Bad_guys_in_game]
        # 得到本局所有邪恶阵营玩家编号
        bad_guys_player_index = []
        for bad_guy in bad_guys_player:
            bad_guys_player_index.append(players_info[bad_guy])
        # 获取相邻数
        start_index = 0
        median = []
        result = []
        for raw_index in range(len(bad_guys_player_index)):
            # 判断是否for循环到指定位置
            if start_index == raw_index:
                # 初始移动位置参数
                index = 0
                while True:
                    # 指针指向的起始值
                    start_value = bad_guys_player_index[start_index]
                    # 如果指针指向最后一个位置，开始值=最后一个值
                    if start_index == bad_guys_player_index[-1]:
                        end_value = start_value
                    else:
                        # 最后一个值 = 初始值 + 位置参数值
                        end_value = bad_guys_player_index[start_index + index]
                    # 通过初始值 + 位置参数值 是否等于 最后一个值，判断是否为相邻数，如果是，添加到列表中
                    if start_value + index == end_value:
                        median.append(end_value)
                        # 位置参数+1
                        index += 1
                    else:
                        # 如果不是，初始指针指向 移动位置参数个单位
                        start_index += index
                    # 把每组相邻数添加到结果列表
                    result.append(median)
        return ["有" + str(len(result)) + "对邪恶阵营玩家座位相邻。"]

def round():
    # 根据配置从角色列表中随机选择个数为[玩家人数]的角色(无重复)
    if players_num == 8:
        # 村民5人，外乡人1，爪牙1，恶魔1
        roles_in_game = sample(Villagers, 5) + sample(Outlanders, 1) + sample(Minions, 1) + sample(Demon, 1)

    players, players_role = build_players(players_num, roles_in_game)
    if first_night and players_num > 7:
        for i in range(players_num):
            # 从[夜晚唤醒顺序]中获得当前使用技能的角色
            current_role = Night_Order_List[i]
            # 仅当角色出现在此局游戏中时才能使用技能
            if current_role in roles_in_game:
                current_player = [k for k, v in players_role.items() if v == current_role][0]
                # 将使用技能获得的信息保存到[玩家信息字典]中
                players_role[current_player].append(Storyteller(current_role, players, players_role))
