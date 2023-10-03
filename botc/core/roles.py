import random
from random import sample
from random import choice
import botc.core.backend as backend
from botc.core.storyteller import storyteller
from botc.core.print import print_to_all
from botc.core.print import print_to_role
from botc.core.print import print_to_grimoire
from botc.core.print import clear_all_print_file
from botc.core.print import print_to_prompt
from botc.core.grimoire import grimoire

# 村民角色
# 洗衣妇 WasherWoman, 图书管理员 librarian, 调查员 investigator, 厨师 cook, 共情者 Empathiser, 占卜师 Soothsayer,
# 送葬者 grave digger, 僧侣 monk, 养鸦人 raven keeper, 圣女 virgin, 杀手 slayer, 士兵 soldier, 市长 mayor
Villagers = ["洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "掘墓人", "僧侣", "养鸦人", "圣女", "杀手",
             "士兵", "市长"]
# 外来人角色
# 管家 butler , 酒鬼 Drunkard, 隐士 Hermit, 圣徒 Saint
Outlanders = ["管家", "酒鬼", "隐士", "圣徒"]
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


def player_input(current_role, alive_list, string):
    player = None
    if current_role == "小恶魔":
        alive_index_list = [i.player_index for i in alive_list]
    else:
        alive_index_list = [i.player_index for i in alive_list if i.true_role != current_role]
    while not isinstance(player, int) or player not in alive_index_list:
        try:
            player = int(input(string + str(alive_index_list)))
            if player < 1 or player > len(alive_index_list):
                print_to_role(current_role, f"请输入玩家编号{alive_index_list}。")
        except ValueError:
            print_to_role(current_role, f"请输入玩家编号{alive_index_list}。")
    return [i for i in alive_list if i.player_index == player][0]


class Role:
    def __init__(self):
        self.true_role = None  # 实际身份
        self.role_for_register = None  # 登记身份
        self.role_for_self = None  # 自己认为的身份
        self.__player_index = None
        self.is_alive = True
        self.toxic = False
        self.info = ""

        self.is_villager = False
        self.is_outlander = False
        self.is_minion = False
        self.is_demon = False
        self.is_traveller = False
        self.is_good_guy = False
        self.is_bad_guy = False

        self.vote_or_not = None

    @property
    def player_index(self):
        return self.__player_index

    @player_index.setter
    def player_index(self, index):
        self.__player_index = index

    def dead(self):
        self.is_alive = False

    def poisoned(self):
        self.toxic = True

    def nominate_input(self, string):
        player_index_list = [i.player_index for i in grimoire.players_list]
        player_input = None
        while not isinstance(player_input, int) or not (player_input in player_index_list or player_input == 0):
            try:
                player_input = int(input(string + str(player_index_list)))
                if player_input < 0 or player_input > len(player_index_list):
                    print_to_role(self.true_role, f"请输入玩家编号{player_index_list},或输入 0 放弃提名。")
            except ValueError:
                print_to_role(self.true_role, f"请输入玩家编号{player_index_list},或输入 0 放弃提名。")
        return player_input

    def nominate(self):
        player_nominated = self.nominate_input(f"你是 玩家{self.player_index} {self.role_for_self}, "
                                               f"请输入玩家编号以提名一位玩家(输入 0 视为放弃提名)：")
        if player_nominated != 0:
            storyteller.player_nominated = [i for i in grimoire.players_list if i.player_index == player_nominated][0]

    def vote_input(self, current_role, string):
        player_input = None
        while not isinstance(player_input, int):
            try:
                player_input = int(input(string))
                if player_input != 0 and player_input != 1:
                    print_to_role(current_role, f"请输入 1 提名投票,或输入 0 不予投票。")
            except ValueError:
                print_to_role(current_role, f"请输入 1 提名投票,或输入 0 不予投票。")
        return player_input

    def vote(self):
        self.vote_or_not = self.vote_input(self.true_role, f"你是{self.player_index} {self.role_for_register}, "
                                                           f"现在对 玩家{storyteller.player_nominated.player_index} "
                                                           f"进行提名投票, 请输入 1 提名投票,或输入 0 不予投票。")

        if self.vote_or_not == 0:
            # 玩家弃票
            grimoire.backend_info.append(f"玩家{self.player_index} 选择弃票")
            print_to_all(f"玩家{self.player_index} 选择弃票")
        else:
            # 玩家投了票
            for player in grimoire.players_list:
                if player.true_role == "管家":
                    if self.true_role == storyteller.butler_to_follow.true_role:
                        player.master_has_voted = self.vote_or_not
            storyteller.nominate_votes += 1
            print_to_all(f"玩家{self.player_index} 选择对 玩家{storyteller.player_nominated.player_index} 的提名进行投票")
            grimoire.backend_info.append(
                f"玩家{self.player_index} {self.true_role} 选择对"
                f" 玩家{storyteller.player_nominated.player_index} {storyteller.player_nominated.true_role}的提名进行投票")
            print_to_grimoire(grimoire.backend_info[-1])


    def skill(self):
        pass


class Washerwoman(Role):
    """
    洗衣妇
    在游戏开始时，洗衣妇会得知某2名玩家中存在某一特定村民身份牌，但不知道具体哪名玩家持有此身份牌。
    返回：list = [村民身份牌，村民身份玩家，另一随机玩家]（两个玩家信息顺序随机）
    """

    def __init__(self):
        super(Washerwoman, self).__init__()
        self.true_role = "洗衣妇"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True

    def skill(self):
        if grimoire.is_night and grimoire.is_first_night:
            player_list = grimoire.players_list
            if self.toxic:
                # 在所有村民(除洗衣妇自身)中随机选择一个身份
                villagers_in_game = [i for i in Villagers if i != "洗衣妇"]
                rand_villager = choice(villagers_in_game)
                # 随机选择两个玩家
                rand_players = sample(player_list, 2)
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 洗衣妇 知道了 {rand_villager} 在 玩家{rand_players[0].player_index} 和 玩家{rand_players[1].player_index} 中。但是他中毒了，因此得到的是错误信息。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"{rand_villager} 在 玩家{rand_players[0].player_index} 和 玩家{rand_players[1].player_index} 中。"
            else:
                # 找出本局所有村民(除洗衣妇自身)并在其中随机选择一个身份(注意使用登记身份)
                villagers_in_game = [i for i in player_list if
                                     i.is_alive and i.role_for_register in Villagers and i.role_for_register != "洗衣妇"]
                villager = choice(villagers_in_game)
                # 再随机选择一个玩家
                player_list_new = [i for i in player_list if i != villager]
                rand_player = choice(player_list)
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 洗衣妇 知道了 {villager.role_for_register} 在 玩家{rand_player.player_index} {rand_player.true_role} 和 玩家{villager.player_index} {villager.true_role} 中。")
                print_to_grimoire(grimoire.backend_info[-1])
                # 打乱身份顺序
                if random.randint(0, 1):
                    self.info = f"{villager.role_for_register} 在 玩家{rand_player.player_index} 和 玩家{villager.player_index} 中。"
                else:
                    self.info = f"{villager.role_for_register} 在 玩家{villager.player_index} 和 玩家{rand_player.player_index} 中。"


class Librarian(Role):
    """
    图书管理员
    在游戏开始时，可得知某2名玩家中存在某一特定外乡人身份牌，但不知道具体哪名玩家持有此身份牌（或得知本局不存在外乡人）。
    返回：["本局游戏没有外乡人。"] 或者 [外乡人身份牌，外乡人身份玩家，另一随机玩家]（两个玩家信息顺序随机）
    """

    def __init__(self):
        super(Librarian, self).__init__()
        self.true_role = "图书管理员"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True

    def skill(self):
        if grimoire.is_night and grimoire.is_first_night:
            player_list = grimoire.players_list
            if self.toxic:
                # 在所有外乡人中随机选择一个身份
                outlander = choice(Outlanders)
                # 随机选择两个玩家
                rand_players = sample(player_list, 2)
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 图书管理员 知道了 {outlander} 在 玩家{rand_players[0].player_index} 和 玩家{rand_players[1].player_index} 中。但是他中毒了，因此得到的是错误信息。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"{outlander} 在 玩家{rand_players[0].player_index} 和 玩家{rand_players[1].player_index} 中。"
            else:
                # 找出本局所有外乡人(注意使用登记身份)
                outlanders_in_game = [i for i in player_list if i.is_alive and i.role_for_register in Outlanders]
                # 如果本局游戏没有外乡人
                if not outlanders_in_game:
                    grimoire.backend_info.append(f"玩家{self.player_index} 图书管理员 知道了本局游戏没有外乡人。")
                    print_to_grimoire(grimoire.backend_info[-1])
                    self.info = "本局游戏没有外乡人。"
                # 如果本局游戏有外乡人，则随机选择一个外乡人身份牌
                else:
                    outlander = choice(outlanders_in_game)
                    # 再随机选择一个角色
                    player_list_new = [i for i in player_list if i.true_role != outlander]
                    rand_player = choice(player_list_new)
                    grimoire.backend_info.append(
                        f"玩家{self.player_index} 图书管理员 知道了 {outlander.true_role} 在 玩家{rand_player.player_index} {rand_player.true_role} 和 玩家{outlander.player_index} {outlander.true_role}中。")
                    print_to_grimoire(grimoire.backend_info[-1])
                    # 打乱身份顺序
                    if random.randint(0, 1):
                        self.info = f"{outlander.true_role} 在 玩家{outlander.player_index} 和 玩家{rand_player.player_index} 中。"
                    else:
                        self.info = f"{outlander.true_role} 在 玩家{rand_player.player_index} 和 玩家{outlander.player_index} 中。"


class Investigator(Role):
    """
    调查员
    在游戏开始时，可得知某2名玩家中存在某一特定爪牙身份牌，但不知道具体哪名玩家为此身份。
    返回：[爪牙身份牌，爪牙身份玩家，另一随机玩家]（两个玩家信息顺序随机）
    """

    def __init__(self):
        super(Investigator, self).__init__()
        self.true_role = "调查员"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True

    def skill(self):
        if grimoire.is_night and grimoire.is_first_night:
            player_list = grimoire.players_list

            if self.toxic:
                # 在所有爪牙中随机选择一个身份
                minions = choice(Minions)
                # 随机选择两个玩家
                rand_players = sample(player_list, 2)
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 调查员 知道了 {minions} 在 玩家{rand_players[0].player_index} 和 玩家{rand_players[1].player_index} 中。但是他中毒了，因此得到的是错误信息。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"{minions} 在 玩家{rand_players[0].player_index} 和 玩家{rand_players[1].player_index} 中。"
            else:
                # 找出本局所有爪牙并在其中随机选择一个身份(注意使用登记身份)
                minions_in_game = [i for i in player_list if i.is_alive and i.role_for_register in Minions]
                minions = choice(minions_in_game)
                # 再随机选择一个角色
                player_list_new = [i for i in player_list if i.true_role != minions]
                rand_player = choice(player_list_new)
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 调查员 知道了 {minions.true_role} 在 玩家{minions.player_index} {minions.true_role} 和 玩家{rand_player.player_index} {rand_player.true_role} 中。")
                print_to_grimoire(grimoire.backend_info[-1])
                # 打乱身份顺序
                if random.randint(0, 1):
                    self.info = f"{minions.true_role} 在 玩家{minions.player_index} 和 玩家{rand_player.player_index} 中。"
                else:
                    self.info = f"{minions.true_role} 在 玩家{rand_player.player_index} 和 玩家{minions.player_index} 中。"


class Cook(Role):
    """
    厨师
    在游戏开始时，可得知有多少对邪恶阵营玩家座位相邻。
    返回：[有{x}对邪恶阵营玩家座位相邻。]
    """

    def __init__(self):
        super(Cook, self).__init__()
        self.true_role = "厨师"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True

    def skill(self):
        if grimoire.is_night and grimoire.is_first_night:
            player_list = grimoire.players_list
            # 找出目前存活的邪恶阵营玩家(注意使用登记身份)
            bad_guys_in_game = [i for i in player_list if i.is_alive and i.role_for_register in Bad_guys]
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
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 厨师 知道了有 {str(result_)} 对邪恶阵营玩家座位相邻。但是他中毒了，因此得到的是错误信息。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = "有 " + str(result_) + " 对邪恶阵营玩家座位相邻。"
            else:
                grimoire.backend_info.append(f"玩家{self.player_index} 厨师 知道了有 {str(result)} 对邪恶阵营玩家座位相邻。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = "有 " + str(result) + " 对邪恶阵营玩家座位相邻。"


class Empath(Role):
    """
    共情者
    每晚都能得知与自己相邻的2位存活玩家（不包括死亡玩家）有几位属于邪恶阵营。
    返回：[与自己相邻的2位存活玩家（不包括死亡玩家）有{x}位属于邪恶阵营。]
    """

    def __init__(self):
        super(Empath, self).__init__()
        self.true_role = "共情者"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True

    def skill(self):
        alive_list = grimoire.alive_list
        if grimoire.is_night:
            # 找出目前存活的邪恶阵营玩家(注意使用登记身份)
            bad_guys_in_game = [i for i in alive_list if i.is_alive and i.role_for_register in Bad_guys]
            # 得到本局所有邪恶阵营玩家编号
            bad_guys_player_index = [i.player_index for i in bad_guys_in_game]
            # 计算与自己相邻的2位存活玩家（不包括死亡玩家）有几位属于邪恶阵营
            result = 0
            if self.player_index == len(alive_list) and 1 in bad_guys_player_index:
                result += 1
            if self.player_index == 1 and len(alive_list) in bad_guys_player_index:
                result += 1
            if self.player_index + 1 in bad_guys_player_index:
                result += 1
            if self.player_index - 1 in bad_guys_player_index:
                result += 1

            if self.toxic:
                result_ = random.randint(0, 2)
                while result_ == result:
                    result_ = random.randint(0, 2)
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 共情者 知道了与自己相邻的2位存活玩家（不包括死亡玩家）有 {str(result_)} 位属于邪恶阵营。但是他中毒了，因此得到的是错误信息。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"与自己相邻的2位存活玩家（不包括死亡玩家）有 {str(result_)} 位属于邪恶阵营。"
            else:
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 共情者 知道了与自己相邻的2位存活玩家（不包括死亡玩家）有 {str(result)} 位属于邪恶阵营。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"与自己相邻的2位存活玩家（不包括死亡玩家）有 {str(result)} 位属于邪恶阵营。"


class Soothsayer(Role):
    """
    占卜师
    每晚都可选择2名玩家得知其中是否存在恶魔身份。但在游戏开始时，会有一名随机玩家（无论身份）被占卜师视为恶魔直到游戏结束，占卜师不知道其真实身份。
    返回：[选择的玩家1, 选择的玩家2, 是否存在恶魔身份]
    """

    def __init__(self):
        super(Soothsayer, self).__init__()
        self.true_role = "占卜师"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True
        self.think_imp = None

    def skill(self):
        if grimoire.is_night:
            if grimoire.is_first_night:
                # 游戏开始时，会有一名随机玩家（无论身份）被占卜师视为恶魔直到游戏结束，占卜师不知道其真实身份。
                players = [i for i in grimoire.players_list if i.true_role != "占卜师"]
                rand_player = choice(players)
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 占卜师 认为 玩家{rand_player.player_index} {rand_player.true_role} 是小恶魔。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.think_imp = rand_player

            alive_list = grimoire.alive_list
            # (注意使用登记身份)
            string = f"你是 玩家{self.player_index} 占卜师，请输入你想占卜的第一位玩家编号："
            player_1 = player_input(self.true_role, alive_list, string)
            string = "请输入你想占卜的第二位玩家编号："
            player_2 = player_input(self.true_role, alive_list, string)
            if self.toxic:
                if player_1.role_for_register in Demon or player_2.role_for_register in Demon:
                    result = " 中不存在恶魔身份。"
                else:
                    result = " 中存在恶魔身份。"
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 占卜师 知道了 玩家{player_1.player_index} {player_1.true_role} 和 玩家{player_2.player_index} {player_2.true_role}" + result + "但是他中毒了，因此得到的是错误信息。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"玩家{player_1.player_index} 和 玩家{player_2.player_index}{result}"
            else:
                if player_1.role_for_register in Demon or player_2.role_for_register in Demon \
                        or self.think_imp.true_role == player_1.true_role or self.think_imp.true_role == player_2.true_role:
                    result = " 中存在恶魔身份。"
                else:
                    result = " 中不存在恶魔身份。"
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 占卜师 知道了 玩家{player_1.player_index} {player_1.true_role} 和 玩家{player_2.player_index} {player_2.true_role}" + result)
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"玩家{player_1.player_index} 和 玩家{player_2.player_index}{result}"


class GraveDigger(Role):
    """
    掘墓人
    掘墓人每晚（除第一晚之外）都能得知当天因处决而死亡的玩家身份。
    返回：[因处决而死亡的玩家身份]
    """

    def __init__(self):
        super(GraveDigger, self).__init__()
        self.true_role = "掘墓人"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True

    def skill(self):
        if grimoire.is_night and not grimoire.is_first_night:
            player_list = grimoire.players_list
            if storyteller.execute_player is not None:
                # (注意使用登记身份)
                if self.toxic:
                    rand_player = choice(player_list)
                    grimoire.backend_info.append(
                        f"玩家{self.player_index} 掘墓人 知道了当天被处决的玩家身份是 {rand_player.role_for_register}。但是他中毒了，因此得到的是错误信息。")
                    print_to_grimoire(grimoire.backend_info[-1])
                    self.info = "白天被处决的玩家身份是 " + rand_player.role_for_register
                else:
                    grimoire.backend_info.append(
                        f"玩家{self.player_index} 掘墓人 知道了当天被处决的玩家身份是 {storyteller.execute_player.role_for_register}。")
                    print_to_grimoire(grimoire.backend_info[-1])
                    self.info = "白天被处决的玩家身份是 " + storyteller.execute_player.role_for_register
            else:
                self.info = "白天没有人被处决"


class Monk(Role):
    """
    僧侣
    僧侣每晚（除第一晚之外）可选择一名除自己之外的玩家，该玩家在当晚不会被恶魔杀死。
    返回：[选择的一名除自己之外的玩家]
    """

    def __init__(self):
        super(Monk, self).__init__()
        self.true_role = "僧侣"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True

    def skill(self):
        if grimoire.is_night and not grimoire.is_first_night:
            alive_list = grimoire.alive_list
            string = f"你是玩家{self.player_index} 僧侣，请输入你今晚想保护的玩家编号："
            storyteller.monk_to_protect = player_input(self.true_role, alive_list, string)
            if self.toxic:
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 僧侣 选择保护 玩家{storyteller.monk_to_protect.player_index}，但是由于他中毒了，因此技能未生效。")
                print_to_grimoire(grimoire.backend_info[-1])
                storyteller.monk_to_protect = None
            else:
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 僧侣 选择保护 玩家{storyteller.monk_to_protect.player_index}。")
                print_to_grimoire(grimoire.backend_info[-1])
            self.info = f"你今晚保护的是 玩家{storyteller.monk_to_protect.player_index}"


class RavenKeeper(Role):
    """
    养鸦人
    如果养鸦人在夜晚死亡，可醒来并选择一名玩家并得知他的身份。
    返回：[选择的一名玩家的登记身份]
    """

    def __init__(self):
        super(RavenKeeper, self).__init__()
        self.true_role = "养鸦人"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True

        self.killed_by_imp = False

    def skill(self):
        if grimoire.is_night and not grimoire.is_first_night:
            if not self.is_alive and self.killed_by_imp:
                self.killed_by_imp = False  # 该技能仅生效一次
                string = f"你是 玩家{self.player_index} 养鸦人，你在夜晚被恶魔杀死，你可以选择一名玩家并得知他的身份："
                player = player_input(self.true_role, grimoire.players_list, string)
                if self.toxic:
                    rand_role = choice(grimoire.players_list).role_for_register
                    grimoire.backend_info.append(
                        f"玩家{self.player_index} 养鸦人 选择查看 玩家{player.player_index} 的身份 {rand_role}, 但是他中毒了，因此得到的是错误信息。")
                    print_to_grimoire(grimoire.backend_info[-1])
                    self.info = f"你今晚选择查看的 玩家{player.player_index} 的 身份是 {rand_role}"
                else:
                    grimoire.backend_info.append(
                        f"玩家{self.player_index} 养鸦人 选择查看 玩家{player.player_index} 的身份是 {player.role_for_register}。")
                    print_to_grimoire(grimoire.backend_info[-1])
                    self.info = f"你今晚选择查看的 玩家{player.player_index} 的 身份是 {player.role_for_register}"


class Virgin(Role):
    """
    圣女
    圣女首次被提名时，若提名者身份为村民，则该村民立即被处决。
    """

    def __init__(self):
        super(Virgin, self).__init__()
        self.true_role = "圣女"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True
        self.nominated = False
        # 圣女技能在storyteller.nomination()中触发。


class Slayer(Role):
    """
    杀手
    杀手在每局游戏仅有一次机会，在白天公开选择一名玩家，若该玩家身份为恶魔，该玩家就会死亡。
    """
    def __init__(self):
        super(Slayer, self).__init__()
        self.true_role = "杀手"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True
        self.player_to_slay = None
        self.skill_has_been_used = False

    def skill(self, use_skill):
        if not grimoire.is_night:
            alive_list = grimoire.alive_list
            if use_skill and not self.skill_has_been_used:
                self.skill_has_been_used = True
                string = f"请输入你想刺杀的玩家编号："
                self.player_to_slay = player_input(self.true_role, alive_list, string)
                grimoire.backend_info.append(f"玩家{self.player_index} 杀手 选择刺杀 玩家{self.player_to_slay.player_index} {self.player_to_slay.true_role}。")
                print_to_grimoire(grimoire.backend_info[-1])
                if self.toxic:
                    grimoire.backend_info.append(f"玩家{self.player_index} 杀手 刺杀 玩家{self.player_to_slay.player_index} {self.player_to_slay.true_role} 时处于中毒状态，因此刺杀失败，无事发生。")
                    print_to_grimoire(grimoire.backend_info[-1])
                    self.info = f"你是 玩家{self.player_index} 杀手, 刺杀 玩家{self.player_to_slay.player_index} 失败，无事发生。"
                    print_to_role(self.true_role, self.info)
                else:
                    if self.player_to_slay.role_for_register == "小恶魔":
                        self.player_to_slay.is_alive = False
                        grimoire.backend_info.append(f"玩家{self.player_index} 杀手 刺杀成功，玩家{self.player_to_slay.player_index} {self.player_to_slay.true_role} 已死亡。")
                        print_to_grimoire(grimoire.backend_info[-1])
                        print_to_all(f"玩家{self.player_index} 刺杀成功，玩家{self.player_to_slay.player_index} 已死亡。")
                        self.info = f"你是 玩家{self.player_index} 杀手, 刺杀 玩家{self.player_to_slay.player_index} 成功，玩家{self.player_to_slay.player_index}已死亡。"
                        print_to_role(self.true_role, self.info)

                        alive_list = [i for i in grimoire.players_list if i.is_alive]
                        grimoire.alive_list = alive_list
                        alive_index_list = [i.player_index for i in grimoire.alive_list]
                        print_to_all(f"目前还存活的玩家编号为：{alive_index_list}")
                    else:
                        grimoire.backend_info.append(f"玩家{self.player_index} 杀手 刺杀 玩家{self.player_to_slay.player_index} {self.player_to_slay.true_role} 失败，无事发生。")
                        print_to_grimoire(grimoire.backend_info[-1])
                        self.info = f"你是 玩家{self.player_index} 杀手, 刺杀 玩家{self.player_to_slay.player_index} 失败，无事发生。"
                        print_to_role(self.true_role, self.info)


class Soldier(Role):
    """
    士兵
    士兵不会被恶魔杀死。
    """

    def __init__(self):
        super(Soldier, self).__init__()
        self.true_role = "士兵"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True
        # 士兵技能在storyteller.check_kill_in_night()中触发。


class Mayor(Role):
    """
    市长
    若只有3名玩家存活且没有玩家被处决，则市长所属阵营获胜；若市长在夜晚被杀，可能会由另一名玩家代替市长死亡。
    """

    def __init__(self):
        super(Mayor, self).__init__()
        self.true_role = "士兵"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_villager = True
        self.is_good_guy = True


class Butler(Role):
    """
    管家
    每晚选择一名除自己外的玩家，次日白天只有该玩家参与的投票管家才能投票，若该玩家不投票，则管家也不能投票。
    返回：[选择的一名玩家]
    """

    def __init__(self):
        super(Butler, self).__init__()
        self.true_role = "管家"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_outlander = True
        self.is_good_guy = True

        self.master_has_voted = None

    def vote(self):
        if self.toxic:
            self.vote_or_not = self.vote_input(self.true_role,
                                               f"你是{self.player_index} {self.role_for_register}, "
                                               f"现在对 玩家{storyteller.player_nominated.player_index} "
                                               f"进行提名投票, 请输入 1 提名投票,或输入 0 不予投票。")
            if self.vote_or_not == 0:
                # 玩家弃票
                # grimoire.backend_info.append(f"玩家{self.player_index} 选择弃票")
                print_to_all(f"玩家{self.player_index} 选择弃票")
            else:
                storyteller.nominate_votes += 1
                print_to_all(f"玩家{self.player_index} 选择投票对 玩家{storyteller.player_nominated.player_index} "
                             f"的提名进行投票")
                grimoire.backend_info.append(
                    f"玩家{self.player_index} {self.true_role} 选择投票对 玩家{storyteller.player_nominated.player_index} "
                    f"{storyteller.player_nominated.true_role} 的提名进行投票")
                print_to_grimoire(grimoire.backend_info[-1])
        else:
            if self.master_has_voted is not None:
                # 主人投了票
                player_to_execute = self.vote_input(self.true_role,
                                                    f"你是玩家{self.player_index} {self.role_for_register}, "
                                                    f"请输入玩家编号以投票处决一位玩家(输入 0 视为弃票)：")
                if player_to_execute == 0:
                    # 玩家弃票
                    # grimoire.backend_info.append(f"玩家{self.player_index} 选择弃票")
                    print_to_all(f"玩家{self.player_index} 选择弃票")
                else:
                    storyteller.nominate_votes += 1
                    print_to_all(f"玩家{self.player_index} 选择投票给 玩家{player_to_execute}")
                    player_to_execute = [i for i in self.players_list if i.player_index == player_to_execute][0]
                    grimoire.backend_info.append(
                        f"玩家{self.player_index} {self.true_role} 选择投票给 玩家{player_to_execute.player_index} {player_to_execute.true_role}")
                    print_to_grimoire(grimoire.backend_info[-1])
            else:
                # 主人没投票
                # grimoire.backend_info.append(f"玩家{self.player_index} 选择弃票")
                print_to_all(f"玩家{self.player_index} 选择弃票")
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 管家, 由于昨晚他选择的主人弃票，因此他也无法投票，视为直接弃票")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"你是 玩家{self.player_index} 管家, 由于昨晚你选择的主人弃票，因此你也无法投票，视为直接弃票"
                print_to_role(self.true_role, self.info)

    def skill(self):
        if grimoire.is_night:
            alive_list = grimoire.alive_list
            string = (f"你是 玩家{self.player_index} 管家，请输入你今晚选择的明天要跟随的投票者的玩家编号：\n"
                      f"(你需要选择一名除自己外的玩家，次日白天只有该玩家参与的投票你才能投票，若该玩家不投票，则你也不能投票。）")
            storyteller.butler_to_follow = player_input(self.true_role, alive_list, string)
            self.info = f"你今晚选择的明天要跟随的投票者是 玩家{storyteller.butler_to_follow.player_index}"
            if self.toxic:
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 管家 选择明天跟随 玩家{storyteller.butler_to_follow.player_index} 投票，但是由于他中毒了，因此技能未生效。")
                print_to_grimoire(grimoire.backend_info[-1])
            else:
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 管家 选择明天跟随 玩家{storyteller.butler_to_follow.player_index} 投票。")
                print_to_grimoire(grimoire.backend_info[-1])


class Drunkard(Role):
    """
    酒鬼
    发到酒鬼身份牌的玩家，会被告知另一个村民身份，并且实际上不知道他的真实身份是酒鬼。该技能是一种永久负面buff。
    """

    def __init__(self):
        super(Drunkard, self).__init__()
        self.true_role = "酒鬼"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_outlander = True
        self.is_good_guy = True

    def skill(self):
        if grimoire.is_first_night:
            # 找出在场的村民角色(这里使用实际身份)
            villagers_in_game = [i.true_role for i in grimoire.players_list if i.is_villager]
            villagers_rest = [i for i in Villagers if i not in villagers_in_game]  # 找出不在场的村民角色
            fake_role = choice(villagers_rest)
            self.role_for_self = fake_role


class Hermit(Role):
    """
    隐士
    隐士可能会被登记为邪恶阵营的爪牙或恶魔，即使死亡。
    """

    def __init__(self):
        super(Hermit, self).__init__()
        self.true_role = "隐士"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_outlander = True
        self.is_good_guy = True

    def skill(self):
        if grimoire.is_night:
            if self.toxic:
                pass
            else:
                rand_num = random.randint(0, 1)
                if rand_num:
                    self.role_for_register = choice(minion_list + demon_list).true_role


class Poisoner(Role):
    """
    投毒者
    每晚可选择一名玩家投毒，当晚和次日白天都会处于中毒状态（中毒会使该玩家身份牌能力暂时消失）。
    返回：[选择要投毒的一名玩家]
    """

    def __init__(self):
        super(Poisoner, self).__init__()
        self.true_role = "投毒者"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_minion = True
        self.is_bad_guy = True

        self.player_to_poison = None

    def skill(self):
        if grimoire.before_game:
            if grimoire.players_num >= 7:
                # 七人或七人以上的局，爪牙与恶魔互相认识但是不知道对方具体身份 ，且恶魔知道三个不在场的好人身份
                bad_players_in_game = [f"玩家{i.player_index}" for i in grimoire.players_list if i.is_bad_guy]
                grimoire.backend_info.append(f"玩家{self.player_index} 投毒者 知道了本局坏人阵营玩家：{bad_players_in_game}")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"本局坏人阵营玩家：{bad_players_in_game}"
        if grimoire.is_night:
            alive_list = grimoire.alive_list
            for i in grimoire.players_list:
                if i.toxic:
                    i.toxic = False
                    grimoire.backend_info.append(f"玩家{i.player_index} {i.true_role} 的毒已经被解开了。")
                    print_to_grimoire(grimoire.backend_info[-1])
            string = f"你是 玩家{self.player_index} 投毒者，请输入你今晚想投毒的玩家编号："
            self.player_to_poison = player_input(self.true_role, alive_list, string)
            grimoire.backend_info.append(
                f"玩家{self.player_index} 投毒者 选择投毒 玩家{self.player_to_poison.player_index} {self.player_to_poison.true_role}")
            print_to_grimoire(grimoire.backend_info[-1])
            self.player_to_poison.toxic = True
            grimoire.backend_info.append(f"玩家{self.player_to_poison.player_index} {self.player_to_poison.true_role} 已被投毒")
            print_to_grimoire(grimoire.backend_info[-1])
            self.info = f"你今晚要投毒的是 玩家{self.player_to_poison.player_index}"


class Spy(Role):
    """
    间谍
    间谍每晚都可以查看魔法书（魔法书记录了每位玩家的实际身份与状态）；间谍可能会被登记为正义阵营的特定身份（村民或外乡人），即使死亡。
    返回：[每位玩家的实际身份与状态]
    """

    def __init__(self):
        super(Spy, self).__init__()
        self.true_role = "间谍"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_minion = True
        self.is_bad_guy = True

    def skill(self):
        if grimoire.before_game:
            if grimoire.players_num >= 7:
                # 七人或七人以上的局，爪牙与恶魔互相认识但是不知道对方具体身份 ，且恶魔知道三个不在场的好人身份
                bad_players_in_game = [f"玩家{i.player_index}" for i in grimoire.players_list if i.is_bad_guy]
                grimoire.backend_info.append(f"玩家{self.player_index} 间谍 知道了本局坏人阵营玩家：{bad_players_in_game}")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"本局坏人阵营玩家：{bad_players_in_game}"
        if grimoire.is_night:
            # 被动技能 间谍可能会被登记为正义阵营的特定身份（村民或外乡人），即使死亡。
            if self.toxic:
                pass
            else:
                rand_num = random.randint(0, 1)
                if rand_num:
                    self.role_for_register = choice(good_guys_list).true_role
            player_list = grimoire.players_list
            # 查看魔法书
            info = ""
            if self.toxic:
                rand_int = random.randint(0, len(player_list))
                for i in range(len(player_list)):
                    rand_player = choice(player_list)
                    player_list_new = [i for i in player_list if i != rand_player]
                    # 随机找一个人中毒
                    if i == rand_int:
                        rand_player.toxic = True
                    else:
                        rand_player.toxic = False
                    # 如果是酒鬼，随机一个他认为自己的身份
                    if rand_player == "酒鬼":
                        villagers_in_game = [i.true_role for i in player_list_new if i.true_role in Villagers]
                        villagers_rest = [i for i in Villagers if i not in villagers_in_game]  # 找出不在场的村民角色
                        fake_role = choice(villagers_rest)
                        info += f"玩家{i} 的实际身份是 {rand_player.true_role}, 他认为自己的身份是 {fake_role}, 他目前{'健康' if not rand_player.toxic else '中毒'}, 醉酒。"
                    else:
                        info += f"玩家{i} 的实际身份是 {rand_player.true_role}, 他目前{'健康' if not rand_player.toxic else '中毒'}。"
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 间谍 查看了魔法书，知道了每位玩家的实际身份与状态。但是他中毒了，因此得到的是错误信息。他得到的错误信息如下：{info}")
                print_to_grimoire(grimoire.backend_info[-1])
            else:
                for player in player_list:
                    if player.true_role == "酒鬼":
                        info += f"玩家{player.player_index} 的实际身份是 {player.true_role}, 他认为自己的身份是 {player.role_for_self}, 他目前{'健康' if not player.toxic else '中毒'}, 醉酒。"
                    else:
                        info += f"玩家{player.player_index} 的实际身份是 {player.true_role}, 他目前{'健康' if not player.toxic else '中毒'}。"
                grimoire.backend_info.append(f"玩家{self.player_index} 间谍 查看了魔法书，知道了每位玩家的实际身份与状态")
                print_to_grimoire(grimoire.backend_info[-1])
            self.info = info


class ScarletWoman(Role):
    """
    猩红女郎
    若场上存在5名或更多玩家存活但恶魔死亡，则猩红女郎会变为恶魔（旅人不算在内）。
    """
    def __init__(self):
        super(ScarletWoman, self).__init__()
        self.true_role = "猩红女郎"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_minion = True
        self.is_bad_guy = True

        self.skill_has_been_used = False

    def skill(self):
        if grimoire.is_night and not grimoire.is_first_night and not self.skill_has_been_used:
            self.skill_has_been_used = True
            imp = [i for i in grimoire.players_list if i.true_role == "小恶魔"][0]
            good_guy_alive_num = len([i for i in grimoire.players_list if i.is_good_guy and i.is_alive])
            if not imp.is_alive and good_guy_alive_num >= 5:
                self.role_for_register = "小恶魔"
                grimoire.backend_info.append(f"玩家{imp.player_index} 小恶魔 已死亡，且场上存活超过5个好人，玩家{self.player_index} 猩红女郎 登记身份已成为 小恶魔。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"小恶魔 已经死亡，且场上存活超过5个好人，你是 猩红女郎 ，你的登记身份已成为 小恶魔。"


class Baron(Role):
    """
    男爵
    可以新增两名外来者，减少两名村民。该技能为游戏开始之前，属于被动技能，只能发动一次。
    """

    def __init__(self):
        super(Baron, self).__init__()
        self.true_role = "男爵"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_minion = True
        self.is_bad_guy = True

    def skill(self):
        if grimoire.before_game:
            if grimoire.players_num >= 7:
                # 七人或七人以上的局，爪牙与恶魔互相认识但是不知道对方具体身份 ，且恶魔知道三个不在场的好人身份
                bad_players_in_game = [f"玩家{i.player_index}" for i in grimoire.players_list if i.is_bad_guy]
                grimoire.backend_info.append(f"玩家{self.player_index} 男爵 知道了本局坏人阵营玩家：{bad_players_in_game}")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"本局坏人阵营玩家：{bad_players_in_game}"

    def passive_skill(self, players_list):
        villagers_in_game = [i for i in players_list if i in villager_list]  # 找出目前在场的村民角色
        villagers_in_game_new = sample(villagers_in_game, len(villagers_in_game) - 2)  # 随机减少两名村民角色
        outlanders_in_game = [i for i in players_list if i in outlander_list]  # 找出目前在场的外乡人角色
        outlanders_in_game_rest = [i for i in outlander_list if i not in outlanders_in_game]  # 找出不在场的外乡人角色
        outlanders_in_game_add = sample(outlanders_in_game_rest, 2)  # 从不在场的外乡人角色中随机添加两名
        outlanders_in_game_new = outlanders_in_game + outlanders_in_game_add
        players_list_rest = [i for i in players_list if i not in villagers_in_game and i not in outlanders_in_game]
        players_list = players_list_rest + villagers_in_game_new + outlanders_in_game_new
        return players_list


class Imp(Role):
    """
    小恶魔
    小恶魔每晚（除第一晚之外）选择一名玩家将其杀死，若选择杀死自己的话，一名爪牙会成为新的小恶魔。
    返回：[选择要杀死的一名玩家]
    """

    def __init__(self):
        super(Imp, self).__init__()
        self.true_role = "小恶魔"
        self.role_for_register = self.true_role
        self.role_for_self = self.true_role
        self.is_demon = True
        self.is_bad_guy = True

    def skill(self):
        if grimoire.before_game:
            if grimoire.players_num >= 7:
                # 七人或七人以上的局，爪牙与恶魔互相认识但是不知道对方具体身份 ，且恶魔知道三个不在场的好人身份
                bad_players_in_game = [f"玩家{i.player_index}" for i in grimoire.players_list if i.is_bad_guy]
                good_not_in_game = [i for i in Good_guys if i not in [r.true_role for r in grimoire.players_list]]
                rand_3_good_not_in_game = sample(good_not_in_game, 3)
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 小恶魔 知道了本局坏人阵营玩家：{bad_players_in_game} 和本局三个不在场的好人身份：{rand_3_good_not_in_game}")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"本局坏人阵营玩家：{bad_players_in_game}, 本局三个不在场的好人身份：{rand_3_good_not_in_game}。"

        if grimoire.is_night and not grimoire.is_first_night:
            alive_list = grimoire.alive_list
            string = f"你是 玩家{self.player_index} 小恶魔，请输入你今晚想杀死的玩家编号："
            storyteller.imp_to_kill = player_input(self.true_role, alive_list, string)
            if self.toxic:
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 小恶魔 选择杀死 玩家{storyteller.imp_to_kill.player_index} {storyteller.imp_to_kill.true_role}，但是由于他中毒了，因此技能未生效。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"你今晚要杀死的是 玩家{storyteller.imp_to_kill.player_index}"
                storyteller.imp_to_kill = None
            else:
                grimoire.backend_info.append(
                    f"玩家{self.player_index} 小恶魔 选择杀死 玩家{storyteller.imp_to_kill.player_index} {storyteller.imp_to_kill.true_role}。")
                print_to_grimoire(grimoire.backend_info[-1])
                self.info = f"你今晚要杀死的是 玩家{storyteller.imp_to_kill.player_index}"


role_list = [Washerwoman(), Librarian(), Investigator(), Cook(), Empath(), Soothsayer(), GraveDigger(), Monk(),
             RavenKeeper(), Virgin(), Slayer(), Soldier(), Butler(), Drunkard(), Hermit(), Poisoner(), Spy(),
             ScarletWoman(), Baron(), Imp()]
# 村民角色
# 洗衣妇 Washerwoman, 图书管理员 librarian, 调查员 investigator, 厨师 cook, 共情者 Empath, 占卜师 Soothsayer,
# 送葬者 grave digger, 僧侣 monk, 养鸦人 raven keeper, 圣女 Virgin, 杀手 slayer, 士兵 soldier, 市长 mayor
villager_list = [Washerwoman(), Librarian(), Investigator(), Cook(), Empath(), Soothsayer(), GraveDigger(), Monk(),
                 RavenKeeper(), Virgin(), Slayer(), Soldier()]
# 外来人角色
# 管家 butler , 酒鬼 Drunkard, 隐士 Hermit, 圣徒 Saint
outlander_list = [Butler(), Drunkard(), Hermit()]
# 爪牙角色
# 投毒者 poisoner, 间谍 spy, 猩红女郎 Scarlet Woman, 男爵 Baron
minion_list = [Poisoner(), Spy(), ScarletWoman(), Baron()]
# 恶魔角色
# 小恶魔 Imp
demon_list = [Imp()]
# 好人阵营
good_guys_list = villager_list + outlander_list
# 坏人阵营
bad_guys_list = minion_list + demon_list
