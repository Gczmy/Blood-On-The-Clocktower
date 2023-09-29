import random
from random import sample
from random import choice
import botc.core.backend as backend

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


class Role:
    def __init__(self):
        self.true_role = None
        self.role = None
        self.__player_index = None
        self.is_alive = True
        self.toxic = False
        self.info = None
        self.fake_info = None

        self.__players_list = None

    @property
    def player_index(self):
        return self.__player_index

    @player_index.setter
    def player_index(self, index):
        self.__player_index = index

    @property
    def players_list(self):
        return self.__players_list

    @players_list.setter
    def players_list(self, players_list):
        self.__players_list = players_list

    def dead(self):
        self.is_alive = False

    def poisoned(self):
        self.toxic = True


class Washerwoman(Role):
    """
    洗衣妇
    在游戏开始时，说书人会告诉洗衣妇某2名玩家中存在某一特定村民身份牌，但不知道具体哪名玩家持有此身份牌。
    返回：list = [村民身份牌，村民身份玩家，另一随机玩家]（两个玩家信息顺序随机）
    """

    def __init__(self):
        super(Washerwoman, self).__init__()
        self.true_role = "洗衣妇"
        self.role = "洗衣妇"

    def skill(self):
        player_list = self.players_list
        if self.toxic:
            # 在所有村民(除洗衣妇自身)中随机选择一个身份
            villagers_in_game = [i for i in Villagers if i != "洗衣妇"]
            villager = choice(villagers_in_game)
            # 随机选择两个玩家
            rand_players = sample(player_list, 2)
            backend.info.append(
                f"洗衣妇 知道了 {villager} 在 {rand_players[1].player_index} 和 {rand_players[2].player_index} 中。但是他中毒了，因此得到是错误信息。")
            self.fake_info = [f"{villager} 在 {rand_players[1]} 和 {rand_players[2]} 中。"]
        else:
            # 找出本局所有村民(除洗衣妇自身)并在其中随机选择一个身份
            villagers_in_game = [i for i in player_list if i.is_alive and i.role in Outlanders and i.role != "洗衣妇"]
            villager = choice(villagers_in_game)
            # 再随机选择一个玩家
            player_list.remove(villager)
            rand_player = choice(player_list)
            backend.info.append(f"洗衣妇 知道了 {villager} 在 {rand_player.player_index} 和 {villager.player_index} 中。")
            # 打乱身份顺序
            if random.randint(0, 1):
                self.info = [f"{villager} 在 {rand_player.player_index} 和 {villager.player_index} 中。"]
            else:
                self.info = [f"{villager} 在 {villager.player_index} 和 {rand_player.player_index} 中。"]


class Librarian(Role):
    """
    图书管理员
    在游戏开始时，可得知某2名玩家中存在某一特定外乡人身份牌，但不知道具体哪名玩家持有此身份牌（或得知本局不存在外乡人）。
    返回：["本局游戏没有外乡人。"] 或者 [外乡人身份牌，外乡人身份玩家，另一随机玩家]（两个玩家信息顺序随机）
    """

    def __init__(self):
        super(Librarian, self).__init__()
        self.true_role = "图书管理员"
        self.role = "图书管理员"

    def skill(self):
        player_list = self.players_list
        if self.toxic:
            # 在所有外乡人中随机选择一个身份
            outlander = choice(Outlanders)
            # 随机选择两个玩家
            rand_players = sample(player_list, 2)
            backend.info.append(
                f"图书管理员 知道了 {outlander} 在 {rand_players[1].player_index} 和 {rand_players[2].player_index} 中。但是他中毒了，因此得到是错误信息。")
            self.fake_info = [f"{outlander} 在 {rand_players[1].player_index} 和 {rand_players[2].player_index} 中。"]
        else:
            # 找出本局所有外乡人
            outlanders_in_game = [i for i in player_list if i.is_alive and i.role in Outlanders]
            # 如果本局游戏没有外乡人
            if not outlanders_in_game:
                backend.info.append(f"图书管理员 知道了本局游戏没有外乡人。")
                self.info = ["本局游戏没有外乡人。"]
            # 如果本局游戏有外乡人，则随机选择一个外乡人身份牌
            else:
                outlander = choice(outlanders_in_game)
                # 再随机选择一个角色
                player_list.remove(outlander)
                rand_player = choice(player_list)
                backend.info.append(f"图书管理员 知道了 {outlander.role} 在 {rand_player.player_index} 和 {outlander.player_index} 中。")
                # 打乱身份顺序
                if random.randint(0, 1):
                    self.info = [f"{outlander.role} 在 {outlander.player_index} 和 {rand_player.player_index} 中。"]
                else:
                    self.info = [f"{outlander.role} 在 {rand_player.player_index} 和 {outlander.player_index} 中。"]


class Investigator(Role):
    """
    调查员
    在游戏开始时，可得知某2名玩家中存在某一特定爪牙身份牌，但不知道具体哪名玩家为此身份。
    返回：[爪牙身份牌，爪牙身份玩家，另一随机玩家]（两个玩家信息顺序随机）
    """

    def __init__(self):
        super(Investigator, self).__init__()
        self.true_role = "调查员"
        self.role = "调查员"

    def skill(self):
        player_list = self.players_list

        if self.toxic:
            # 在所有爪牙中随机选择一个身份
            minions = choice(Minions)
            # 随机选择两个玩家
            rand_players = sample(player_list, 2)
            backend.info.append(
                f"调查员 知道了 {minions} 在 {rand_players[1].player_index} 和 {rand_players[2].player_index} 中。但是他中毒了，因此得到是错误信息。")
            self.fake_info = [f"{minions} 在 {rand_players[1].player_index} 和 {rand_players[2].player_index} 中。"]
        else:
            # 找出本局所有爪牙并在其中随机选择一个身份
            minions_in_game = [i for i in player_list if i.is_alive and i.role in Minions]
            minions = choice(minions_in_game)
            # 再随机选择一个角色
            player_list.remove(minions)
            rand_player = choice(player_list)
            backend.info.append(f"调查员 知道了 {minions.role} 在 玩家{minions.player_index} 和 玩家{rand_player.player_index} 中。")
            # 打乱身份顺序
            if random.randint(0, 1):
                self.info = [f"{minions.role} 在 玩家{minions.player_index} 和 玩家{rand_player.player_index} 中。"]
            else:
                self.info = [f"{minions.role} 在 玩家{rand_player.player_index} 和 玩家{minions.player_index} 中。"]


class Cook(Role):
    """
    厨师
    在游戏开始时，可得知有多少对邪恶阵营玩家座位相邻。
    返回：[有{x}对邪恶阵营玩家座位相邻。]
    """

    def __init__(self):
        super(Cook, self).__init__()
        self.true_role = "厨师"
        self.role = "厨师"

    def skill(self):
        player_list = self.players_list
        # 找出目前存活的邪恶阵营玩家
        bad_guys_in_game = [i for i in player_list if i.is_alive and i.role in Bad_guys]
        # 得到本局所有邪恶阵营玩家编号
        bad_guys_player_index = [i.player_index for i in bad_guys_in_game]
        # 获取相邻数
        # 遍历列表中的元素，检查每个元素是否满足相邻数的条件
        result = 0
        for num in bad_guys_player_index:
            if num == len(player_list) and 1 in bad_guys_player_index:
                result += 1
            if num + 1 in bad_guys_player_index:
                result += 1

        if self.toxic:
            result_ = random.randint(0, 3)
            while result_ == result:
                result_ = random.randint(0, 3)
            backend.info.append(f"厨师 知道了有 {str(result_)} 对邪恶阵营玩家座位相邻。但是他中毒了，因此得到是错误信息。")
            self.fake_info = ["有 " + str(result_) + " 对邪恶阵营玩家座位相邻。"]
        else:
            backend.info.append(f"厨师 知道了有 {str(result)} 对邪恶阵营玩家座位相邻。")
            self.info = ["有 " + str(result) + " 对邪恶阵营玩家座位相邻。"]


class Empath(Role):
    """
    共情者
    每晚都能得知与自己相邻的2位存活玩家（不包括死亡玩家）有几位属于邪恶阵营。
    返回：[与自己相邻的2位存活玩家（不包括死亡玩家）有{x}位属于邪恶阵营。]
    """

    def __init__(self):
        super(Empath, self).__init__()
        self.true_role = "共情者"
        self.role = "共情者"

    def skill(self):
        player_list = self.players_list
        alive_player_list = [i for i in player_list if i.is_alive]
        # 找出目前存活的邪恶阵营玩家
        bad_guys_in_game = [i for i in alive_player_list if i.is_alive and i.role in Bad_guys]
        # 得到本局所有邪恶阵营玩家编号
        bad_guys_player_index = [i.player_index for i in bad_guys_in_game]
        # 计算与自己相邻的2位存活玩家（不包括死亡玩家）有几位属于邪恶阵营
        result = 0
        if self.player_index == len(alive_player_list) and 1 in bad_guys_player_index:
            result += 1
        if self.player_index == 1 and len(alive_player_list) in bad_guys_player_index:
            result += 1
        if self.player_index + 1 in bad_guys_player_index:
            result += 1
        if self.player_index - 1 in bad_guys_player_index:
            result += 1

        if self.toxic:
            result_ = random.randint(0, 2)
            while result_ == result:
                result_ = random.randint(0, 2)
            backend.info.append(f"共情者 知道了与自己相邻的2位存活玩家（不包括死亡玩家）有 {str(result_)} 位属于邪恶阵营。但是他中毒了，因此得到是错误信息。")
            self.fake_info = [f"与自己相邻的2位存活玩家（不包括死亡玩家）有 {str(result_)} 位属于邪恶阵营。"]
        else:
            backend.info.append(f"共情者 知道了与自己相邻的2位存活玩家（不包括死亡玩家）有 {str(result)} 位属于邪恶阵营。")
            self.info = [f"与自己相邻的2位存活玩家（不包括死亡玩家）有 {str(result)} 位属于邪恶阵营。"]


class Soothsayer(Role):
    """
    占卜师
    每晚都可选择2名玩家得知其中是否存在恶魔身份。但在游戏开始时，会有一名随机玩家（无论身份）被占卜师视为恶魔直到游戏结束，占卜师不知道其真实身份。
    返回：[选择的玩家1, 选择的玩家2, 是否存在恶魔身份]
    """

    def __init__(self):
        super(Soothsayer, self).__init__()
        self.true_role = "共情者"
        self.role = "共情者"

    def skill(self, player_1, player_2):
        player_list = self.players_list
        if self.toxic:
            if player_1.role in Demon or player_2.role in Demon:
                result = " 中不存在恶魔身份。"
            else:
                result = " 中存在恶魔身份。"
            backend.info.append(f"占卜师 知道了 {player_1} 和 {player_2}" + result + "但是他中毒了，因此得到的是错误信息。")
            self.fake_info = [player_1 + " 和 " + player_2 + result]
        else:
            if player_1.role in Demon or player_2.role in Demon:
                result = " 中存在恶魔身份。"
            else:
                result = " 中不存在恶魔身份。"
            backend.info.append(f"占卜师 知道了 {player_1} 和 {player_2}" + result)
            self.info = [player_1 + " 和 " + player_2 + result]
