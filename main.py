import random
from random import sample
from random import choice
from collections import Counter
from icecream import ic
ic.enable()


# 村民角色
# 洗衣妇 WasherWoman, 图书管理员 librarian, 调查员 investigator, 厨师 cook, 共情者 Empathiser, 占卜师 Soothsayer,
# 送葬者 grave digger, 僧侣 monk, 养鸦人 crow raiser, 处女 virgin, 杀手 killer, 军人 soldier, 市长 mayor
Villagers = ["洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "掘墓人", "僧侣", "养鸦人", "处女", "杀手",
             "军人", "市长"]
# 外来人角色
# 管家 butler , 酒鬼 Drunkard, 隐士 Hermit, 圣人 Saint
Outlanders = ["管家", "酒鬼", "隐士", "圣人"]
# 爪牙角色
# 投毒者 poisoner, 间谍 spy, 猩红女郎 Scarlet Woman, 男爵 Baron
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


def build_players(players_num, roles_in_game):
    roles_in_game = roles_in_game.copy()

    players_info = {}  # 玩家信息字典: key:玩家代号, value:[0]玩家编号，[1]玩家自身身份，[2]玩家存活信息，[3~n]玩家使用技能得到的信息
    players = []  # 玩家代号
    for i in range(players_num):
        players.append("玩家" + str(i + 1))
        # 为玩家随机选择配置中的角色
        role = choice(roles_in_game)
        # role = roles_in_game[0]
        players_info[players[i]] = [i + 1, role, "存活"]
        roles_in_game.remove(role)
    return players, players_info


# 夜晚唤醒顺序：投毒者＞恶魔＞洗衣妇＞图书管理员＞调查员＞厨师＞共情者＞占卜师＞管家＞间谍，若场上无该角色，可直接顺延
Night_Order_List = ["投毒者", "小恶魔", "洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "管家", "间谍"]


def washerwoman(player, players, players_info):
    """
    洗衣妇
    在游戏开始时，说书人会告诉洗衣妇某2名玩家中存在某一特定村民身份牌，但不知道具体哪名玩家持有此身份牌。
    返回：list = [村民身份牌，村民身份玩家，另一随机玩家]（两个玩家信息顺序随机）
    """
    players = players.copy()
    # 先将使用技能的角色自身排除在列表之外
    players.remove(player)

    # 找出本局所有村民并在其中随机选择一个
    Villagers_in_game = []
    for i in players_info.values():
        if i[1] in Villagers:
            Villagers_in_game.append(i[1])
    villager = choice(Villagers_in_game)
    villager_player = [k for k, v in players_info.items() if v[1] == villager][0]
    # 再随机选择一个角色
    players.remove(villager_player)
    rand_player = choice(players)
    # 打乱身份顺序
    if random.randint(0, 1):
        return [villager, rand_player, villager_player]
    else:
        return [villager, villager_player, rand_player]


def librarian(player, players, players_info):
    """
    图书管理员
    在游戏开始时，可得知某2名玩家中存在某一特定外乡人身份牌，但不知道具体哪名玩家持有此身份牌（或得知本局不存在外乡人）。
    返回：["本局游戏没有外乡人。"] 或者 [外乡人身份牌，外乡人身份玩家，另一随机玩家]（两个玩家信息顺序随机）
    """
    players = players.copy()
    # 先将使用技能的角色自身排除在列表之外
    players.remove(player)

    Outlanders_in_game = []
    # 找出本局所有外乡人
    for i in players_info.values():
        if i[1] in Outlanders:
            Outlanders_in_game.append(i[1])
    # 如果本局游戏没有外乡人
    if not Outlanders_in_game:
        return ["本局游戏没有外乡人。"]
    # 如果本局游戏有外乡人，则随机选择一个外乡人身份牌
    else:
        outlander = choice(Outlanders_in_game)
        outlander_player = [k for k, v in players_info.items() if v[1] == outlander][0]
        # 再随机选择一个角色
        players.remove(outlander_player)
        rand_player = choice(players)
        # 打乱身份顺序
        if random.randint(0, 1):
            return [f"{outlander} 在 {rand_player} 和 {outlander_player} 中"]
        else:
            return [f"{outlander} 在 {outlander_player} 和 {rand_player} 中"]


def investigator(player, players, players_info):
    """
    调查员
    在游戏开始时，可得知某2名玩家中存在某一特定爪牙身份牌，但不知道具体哪名玩家为此身份。
    返回：[爪牙身份牌，爪牙身份玩家，另一随机玩家]（两个玩家信息顺序随机）
    """
    players = players.copy()
    # 先将使用技能的角色自身排除在列表之外
    players.remove(player)

    Minions_in_game = []
    # 找出本局所有爪牙并在其中随机选择一个
    for i in players_info.values():
        if i[1] in Minions:
            Minions_in_game.append(i[1])
    minions = choice(Minions_in_game)
    minions_player = [k for k, v in players_info.items() if v[1] == minions][0]
    # 再随机选择一个角色
    players.remove(minions_player)
    rand_player = choice(players)
    # 打乱身份顺序
    if random.randint(0, 1):
        return [f"{minions} 在 {minions_player} 和 {rand_player} 中。"]
    else:
        return [f"{minions} 在 {rand_player} 和 {minions_player} 中。"]


def cook(players, players_info):
    """
    厨师
    在游戏开始时，可得知有多少对邪恶阵营玩家座位相邻。
    返回：[有{x}对邪恶阵营玩家座位相邻。]
    """
    Bad_guys_in_game = []
    # 找出本局所有邪恶阵营角色和对应玩家
    for i in players_info.values():
        if i[1] in Bad_guys:
            Bad_guys_in_game.append(i[1])
    bad_guys_players = [k for k, v in players_info.items() if v[1] in Bad_guys_in_game]
    # 得到本局所有邪恶阵营玩家编号
    bad_guys_player_index = []
    for bad_guy in bad_guys_players:
        bad_guys_player_index.append(players_info[bad_guy][0])
    # 获取相邻数
    # 遍历列表中的元素，检查每个元素是否满足相邻数的条件
    result = 0
    for num in bad_guys_player_index:
        if num == len(players) and 1 in bad_guys_player_index:
            result += 1
        if num + 1 in bad_guys_player_index:
            result += 1
    return ["有 " + str(result) + " 对邪恶阵营玩家座位相邻。"]


def empathiser(role, players_info):
    """
    共情者
    每晚都能得知与自己相邻的2位存活玩家（不包括死亡玩家）有几位属于邪恶阵营。
    返回：[与自己相邻的2位存活玩家（不包括死亡玩家）有{x}位属于邪恶阵营。]
    """
    Bad_guys_in_game = []
    # 找出目前存活的邪恶阵营角色和对应玩家
    alive_num = 0  # 存活玩家人数
    for i in players_info.values():
        if i[2] == "存活":
            alive_num += 1
            if i[1] in Bad_guys:
                Bad_guys_in_game.append(i[1])
    bad_guys_players = [k for k, v in players_info.items() if v[1] in Bad_guys_in_game]
    # 得到本局所有邪恶阵营玩家编号
    bad_guys_player_index = []
    for bad_guy in bad_guys_players:
        bad_guys_player_index.append(players_info[bad_guy][0])
    # 得到自身编号
    self_index = [v[0] for k, v in players_info.items() if v[1] == role][0]
    # 计算与自己相邻的2位存活玩家（不包括死亡玩家）有几位属于邪恶阵营
    result = 0
    if self_index == alive_num and 1 in bad_guys_player_index:
        result += 1
    if self_index == 1 and alive_num in bad_guys_player_index:
        result += 1
    if self_index + 1 in bad_guys_player_index:
        result += 1
    if self_index - 1 in bad_guys_player_index:
        result += 1
    return [f"与自己相邻的2位存活玩家（不包括死亡玩家）有 {str(result)} 位属于邪恶阵营。"]


def soothsayer(players_info, Soothsayer_player_1, Soothsayer_player_2):
    """
    占卜师
    每晚都可选择2名玩家得知其中是否存在恶魔身份。但在游戏开始时，会有一名随机玩家（无论身份）被占卜师视为恶魔直到游戏结束，占卜师不知道其真实身份。
    返回：[选择的玩家1, 选择的玩家2, 是否存在恶魔身份]
    """
    role_1 = [v[1] for k, v in players_info.items() if v[0] == Soothsayer_player_1][0]
    role_2 = [v[1] for k, v in players_info.items() if v[0] == Soothsayer_player_2][0]
    player_1 = [k for k, v in players_info.items() if v[0] == Soothsayer_player_1][0]
    player_2 = [k for k, v in players_info.items() if v[0] == Soothsayer_player_2][0]
    if role_1 in Demon or role_2 in Demon:
        result = " 中存在恶魔身份"
    else:
        result = " 中不存在恶魔身份"
    return [player_1 + " 和 " + player_2 + result]


def grave_digger(players_info, execute_player):
    """
    掘墓人
    掘墓人每晚（除第一晚之外）都能得知当天因处决而死亡的玩家身份。
    返回：[因处决而死亡的玩家身份]
    """
    role = [v[1] for k, v in players_info.items() if v[0] == execute_player][0]
    return ["白天被处决的是 " + role]


def monk(players_info, player_to_protect):
    """
    僧侣
    僧侣每晚（除第一晚之外）可选择一名除自己之外的玩家，该玩家在当晚不会被恶魔杀死。
    返回：[选择的一名除自己之外的玩家]
    """
    player = [k for k, v in players_info.items() if v[0] == player_to_protect][0]
    return ["你今晚保护的是" + player]


def butler(players_info, player_to_vote):
    """
    管家
    每晚选择一名除自己外的玩家，次日白天只有该玩家参与的投票管家才能投票，若该玩家不投票，则管家也不能投票。
    返回：[选择的一名玩家]
    """
    player = [k for k, v in players_info.items() if v[0] == player_to_vote][0]
    return ["你今晚选择的明天要跟随的投票者是 " + player]


def poisoner(players_info, player_to_poison):
    """
    投毒者
    每晚可选择一名玩家投毒，当晚和次日白天都会处于中毒状态（中毒会使该玩家身份牌能力暂时消失）。
    返回：[选择要投毒的一名玩家]
    """
    player = [k for k, v in players_info.items() if v[0] == player_to_poison][0]
    return ["你今晚要投毒的是 " + player]


def spy(players_info):
    """
    间谍
    间谍每晚都可以查看魔法书（魔法书记录了每位玩家的实际身份与状态）；间谍可能会被登记为正义阵营的特定身份（村民或外乡人），即使死亡。
    返回：[每位玩家的实际身份与状态]
    """
    # 查看魔法书
    info = []
    for v in players_info.values():
        info.append([v[0], v[1], v[2]])
    return info


def imp(players_info, player_to_kill):
    """
    小恶魔
    小恶魔每晚（除第一晚之外）选择一名玩家将其杀死，若选择杀死自己的话，一名爪牙会成为新的小恶魔。
    返回：[选择要杀死的一名玩家]
    """
    player = [k for k, v in players_info.items() if v[0] == player_to_kill][0]
    return ["你今晚要杀死的是 " + player]


def storyteller(players,
                players_info,
                execute_player=None,
                player_to_poison=None,
                player_1=None,
                player_2=None,
                player_to_vote=None,
                player_to_protect=None,
                player_to_kill=None):
    """
    说书人
    """
    if execute_player:
        player = [k for k, v in players_info.items() if v[0] == execute_player][0]
        players_info[player][2] = "死亡"
    if player_to_kill:
        if player_to_protect:
            role_to_kill = [v[1] for k, v in players_info.items() if v[0] == player_to_kill][0]
            role_to_protect = [v[1] for k, v in players_info.items() if v[0] == player_to_protect][0]
            if role_to_protect == role_to_kill:
                if role_to_protect == "市长":
                    print(f"公示信息：僧侣 保护了【市长】，小恶魔 选择杀死【市长】，市长的“另一名玩家替代死亡”能力不会触发，"
                          f"因为【市长】当晚不会被恶魔杀死。当晚没有人死亡")
                elif role_to_protect == "小恶魔":
                    print(
                        f"公示信息：僧侣保护了【小恶魔】，【小恶魔】选择当晚杀死自己，但什么也没有发生。【小恶魔】依然存活，"
                        f"并且没有出现新的【小恶魔】")
                else:
                    print(f"公示信息：僧侣 保护了 {role_to_protect}，小恶魔 选择杀死 {role_to_kill}，当晚没有人死亡")
        else:
            player = [k for k, v in players_info.items() if v[0] == player_to_kill][0]
            players_info[player][2] = "死亡"

    return players_info


def player_index_input(alive_list, players_info, current_player, string):
    alive_list = alive_list.copy()
    current_player_index = players_info[current_player][0]
    alive_list.remove(current_player_index)
    player_input = None
    while not isinstance(player_input, int) or not player_input in alive_list:
        try:
            player_input = int(input(string + str(alive_list)))
            if player_input < 1 or player_input > len(alive_list):
                print(f"请输入玩家编号{alive_list}。")
        except ValueError:
            print(f"请输入玩家编号{alive_list}。")
    return player_input


def first_night(alive_roles_in_game, alive_list, players, players_info):
    player_to_poison = 0
    player_1 = 0
    player_2 = 0
    player_to_vote = 0
    # 从[夜晚唤醒顺序]中获得当前使用技能的角色
    for current_role in Night_Order_List:
        # 仅当角色出现在此局游戏中时才能使用技能
        if current_role in alive_roles_in_game:
            current_player = [k for k, v in players_info.items() if v[1] == current_role][0]
            info = []
            # 角色使用技能
            if current_role == "投毒者":
                player_to_poison = player_index_input(alive_list, players_info, current_player, "你的角色是投毒者，请输入你今晚想投毒的玩家编号：")
                info = poisoner(players_info, player_to_poison)
            if current_role == "洗衣妇":
                info = washerwoman(current_player, players, players_info)
            if current_role == "图书管理员":
                info = librarian(current_player, players, players_info)
            if current_role == "调查员":
                info = investigator(current_player, players, players_info)
            if current_role == "厨师":
                info = cook(players_info)
            if current_role == "共情者":
                info = empathiser(current_role, players_info)
            if current_role == "占卜师":
                # 游戏开始时，会有一名随机玩家（无论身份）被占卜师视为恶魔直到游戏结束，占卜师不知道其真实身份。
                players_ = players.copy()
                players_.remove(current_player)
                rand_player = choice(players_)
                players_info[current_player].append(["你认为 " + rand_player + " 是小恶魔。"])
                player_1 = player_index_input(alive_list, players_info, current_player, "你的角色是占卜师，请输入你想占卜的第一位玩家编号：")
                player_2 = player_index_input(alive_list, players_info, current_player, "请输入你想占卜的第二位玩家编号：")
                info = soothsayer(players_info, player_1, player_2)
            if current_role == "管家":
                player_to_vote = player_index_input(alive_list, players_info, current_player, "你的角色是管家，请输入你今晚选择的明天要跟随的投票者的玩家编号："
                                                             "（你需要选择一名除自己外的玩家，次日白天只有该玩家参与的投票你才能投票，"
                                                             "若该玩家不投票，则你也不能投票。）")
                info = butler(players_info, player_to_vote)
            if current_role == "间谍":
                info = spy(players_info)
            # 将使用技能获得的信息保存到[玩家信息字典]中
            players_info[current_player].append(info)
    return players_info, player_to_poison, player_1, player_2, player_to_vote


def other_nights(alive_roles_in_game, alive_list, players, players_info, execute_player):
    player_to_protect = 0
    player_to_kill = 0
    # 从[夜晚唤醒顺序]中获得当前使用技能的角色
    for current_role in Night_Order_List:
        # 仅当角色存活时才能使用技能
        if current_role in alive_roles_in_game:
            info = []
            current_player = [k for k, v in players_info.items() if v[1] == current_role][0]
            if current_role == "僧侣":
                player_to_protect = player_index_input(alive_list, players_info, current_player, "你的角色是僧侣，请输入你今晚想保护的玩家编号：")
                info = monk(players_info, player_to_protect)
            if current_role == "小恶魔":
                player_to_kill = player_index_input(alive_list, players_info, current_player, "你的角色是小恶魔，请输入你今晚想杀死的玩家编号：")
                info = imp(players_info, player_to_kill)
            if current_role == "掘墓人":
                info = grave_digger(players_info, execute_player)
            # 将使用技能获得的信息保存到[玩家信息字典]中
            players_info[current_player].append(info)
    return players_info, player_to_protect, player_to_kill


def check_alive(players_info):
    alive_list = []
    alive_roles_in_game = []
    for v in players_info.values():
        if v[2] == "存活":
            alive_list.append(v[0])
            alive_roles_in_game.append(v[1])
    print("目前还存活的玩家编号为：", alive_list)
    return alive_roles_in_game, alive_list


def game():
    # 玩家人数
    players_num = 8

    good_guys_win = False
    bad_guys_win = False
    # 根据配置从角色列表中随机选择个数为[玩家人数]的角色(无重复)
    if players_num == 8:
        # 村民5人，外乡人1，爪牙1，恶魔1
        roles_in_game = sample(Villagers, 5) + sample(Outlanders, 1) + sample(Minions, 1) + sample(Demon, 1)
        alive_roles_in_game = sample(Villagers, 5) + sample(Outlanders, 1) + sample(Minions, 1) + sample(Demon, 1)
    roles_in_game = ["小恶魔", "投毒者", "调查员", "间谍", "共情者", "占卜师", "管家", "僧侣"]

    players, players_info = build_players(players_num, roles_in_game)
    is_first_night = True
    is_night = True
    print("游戏开始")
    ic(players_info)
    while not good_guys_win and not bad_guys_win:
        if is_night:
            print("现在是晚上")
            player_to_poison = 0
            player_1 = 0
            player_2 = 0
            player_to_vote = 0
            player_to_protect = 0
            player_to_kill = 0
            alive_roles_in_game, alive_list = check_alive(players_info)
            if is_first_night:
                is_first_night = False
                is_night = False
                if players_num > 7:
                    ic("七人或七人以上的局，爪牙与恶魔互相认识但是不知道对方具体身份 ，且恶魔知道三个不在场的身份")
                    bad_guys_in_game = [v[1] for k, v in players_info.items() if v[1] in Bad_guys]
                    bad_players_in_game = [k for k, v in players_info.items() if v[1] in Bad_guys]
                    ic(bad_guys_in_game)
                    ic(bad_players_in_game)
                    for player in bad_players_in_game:
                        players_info[player].append(f"本局坏人阵营玩家：{bad_players_in_game}")
                        if players_info[player][1] == "小恶魔":
                            role_not_in_game = [r for r in roles_all if r not in roles_in_game]
                            rand_3_role_not_in_game = sample(role_not_in_game, 3)
                            players_info[player].append(f"本局三个不在场的身份：{rand_3_role_not_in_game}")

                    ic(players_info)
                    players_info, player_to_poison, player_1, player_2, player_to_vote = first_night(alive_roles_in_game, alive_list, players, players_info)
            else:
                is_night = False
                players_info, player_to_protect, player_to_kill = other_nights(alive_roles_in_game, alive_list, players, players_info, execute_player)

        else:
            is_night = True
            players_info = storyteller(players=players,
                                       players_info=players_info,
                                       player_to_poison=player_to_poison,
                                       player_1=player_1,
                                       player_2=player_2,
                                       player_to_vote=player_to_vote,
                                       player_to_protect=player_to_protect,
                                       player_to_kill=player_to_kill)
            print("现在是白天")
            alive_roles_in_game, alive_list = check_alive(players_info)
            player_vote_list = []
            for current_role in roles_in_game:
                current_player = [k for k, v in players_info.items() if v[1] == current_role][0]
                player_vote_list.append(player_index_input(alive_list, players_info, current_player, f"你是{current_role}, "
                                                                    f"请输入玩家编号以投票处决一位玩家："))
            vote_counts = Counter(player_vote_list)
            most_common_vote = vote_counts.most_common(1)
            execute_player = most_common_vote[0][0]
            players_info = storyteller(players=players,
                                       players_info=players_info,
                                       execute_player=execute_player)


game()
