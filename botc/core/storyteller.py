from collections import Counter
import botc.core.backend as backend
from botc.core.print import print_to_all
from botc.core.print import print_to_role
from botc.core.print import clear_all_print_file
from botc.core.print import print_to_prompt
from botc.core.print import print_to_backend
from botc.core.grimoire import grimoire


class Storyteller:
    def __init__(self):
        self.butler_to_follow = None
        self.monk_to_protect = None
        self.imp_to_kill = None
        self.nominate_votes = 0
        self.execute_player = None
        self.killed_last_night = None
        self.nominate_list = []
        self.votes_list = []
        self.player_nominated = None

    def check_kill_in_night(self):
        if self.imp_to_kill is not None:
            if self.monk_to_protect != self.imp_to_kill:
                if self.imp_to_kill.true_role == "士兵":
                    if self.imp_to_kill.toxic:
                        self.imp_to_kill.dead()
                        self.killed_last_night = self.imp_to_kill
                        backend.info.append(
                            f"玩家{self.imp_to_kill.player_index} {self.imp_to_kill.true_role} 被小恶魔杀死, 由于士兵中毒, 士兵技能失效。")
                    else:
                        # 士兵不会被恶魔杀死。
                        backend.info.append(
                            f"小恶魔选择杀死 玩家{self.imp_to_kill.player_index} {self.imp_to_kill.true_role}，"
                            f"触发了士兵的技能，没有人死亡。")
                # 小恶魔选择杀死的人和僧侣选择保护的人不是同一个人, 则被小恶魔选择杀死的人死亡
                self.imp_to_kill.dead()
                if self.imp_to_kill.true_role == "养鸦人":
                    self.imp_to_kill.killed_by_imp = True
                self.killed_last_night = self.imp_to_kill
                backend.info.append(f"玩家{self.imp_to_kill.player_index} {self.imp_to_kill.true_role} 被小恶魔杀死。")
            self.imp_to_kill = None
            self.monk_to_protect = None

    def check_kill_in_daytime(self):
        if self.killed_last_night is None:
            print_to_all(f"昨晚没有玩家死亡。")
        else:
            print_to_all(f"昨晚 玩家{self.killed_last_night.player_index} 死亡。")
        self.killed_last_night = None

    def nomination(self):
        print_to_all("提名开始")
        alive_list = [i for i in grimoire.players_list if i.is_alive]
        for player in alive_list:
            player.nominate()
            if self.player_nominated is not None:
                print_to_all(f"玩家{player.player_index} 提名了 玩家{self.player_nominated.player_index}。")
                print_to_backend(f"玩家{player.player_index} {player.true_role} 提名了 玩家{self.player_nominated.player_index} {self.player_nominated.true_role}。")
                if self.player_nominated.true_role == "圣女":
                    if self.player_nominated.toxic:
                        print_to_backend(
                            f"玩家{player.player_index} 提名了 圣女，圣女中毒了，圣女技能视为被使用，正常进行提名投票。")
                    else:
                        if not self.player_nominated.nominated:
                            # 圣女首次被提名
                            self.player_nominated.nominated = True
                            # 圣女首次被提名时，若提名者身份为村民，则该村民立即被处决, 且白天结束。
                            if player.is_villager:
                                player.dead()
                                print_to_all(f"玩家{player.player_index} 被处决，白天结束。")
                                print_to_backend(f"玩家{player.player_index} {player.true_role} 由于圣女技能触发被处决，白天结束。")
                                return
                            else:
                                print_to_backend(f"玩家{player.player_index} 提名了 圣女，提名者身份不是村民，圣女技能视为被使用，正常进行提名投票。")
                # 对该提名进行投票
                self.vote_to_execute()
                self.player_nominated = None
        self.check_votes()

    def vote_to_execute(self):
        print_to_all(f"对提名 玩家{self.player_nominated.player_index} 的投票开始。")
        alive_list = [i for i in grimoire.players_list if i.is_alive]
        butler = None
        for player in alive_list:
            if player.true_role == "管家":
                # 如果管家活着，将管家放到列表的最后，确保管家在主人之后投票
                butler = player
                continue
            player.vote()
        if butler is not None:
            butler.vote()
        print_to_all(f"对提名 玩家{self.player_nominated.player_index} 的投票结束。")
        self.nominate_list.append(self.player_nominated)
        self.votes_list.append(self.nominate_votes)

    def check_votes(self):
        # 唱票
        vote_counts = Counter(self.votes_list)
        if self.votes_list:
            m1 = max(self.votes_list)
            if m1 == 0:
                backend.info.append(f"所有玩家弃票，没有玩家被处决")
                print_to_all(f"所有玩家弃票，没有玩家被处决")
            else:
                if len(self.votes_list) > 1:
                    # 如果被提名的不止一个
                    votes_list = self.votes_list.copy()
                    votes_list.remove(m1)
                    m2 = max(votes_list)
                    if m1 == m2:
                        backend.info.append(f"玩家平票，没有玩家被处决")
                        print_to_all(f"玩家平票，没有玩家被处决")
                    else:
                        execute_player = self.nominate_list[self.votes_list.index(m1)]
                        print_to_all(f"玩家{execute_player.player_index} 票数最多，被处决")
                        backend.info.append(f"玩家{execute_player.player_index} {execute_player.true_role} 票数最多，被处决")
                        execute_player.dead()
                else:
                    execute_player = self.nominate_list[self.votes_list.index(m1)]
                    print_to_all(f"玩家{execute_player.player_index} 票数最多，被处决")
                    backend.info.append(f"玩家{execute_player.player_index} {execute_player.true_role} 票数最多，被处决")
                    execute_player.dead()
        else:
            backend.info.append(f"没有玩家被提名，没有玩家被处决")
            print_to_all(f"没有玩家被提名，没有玩家被处决")

        # Todo:统计票数环节可以让玩家们退票，如果主人退票，管家也必须退票
        self.nominate_list = []
        self.votes_list = []
        self.nominate_votes = 0

    def check_daytime_skill(self):
        for player in grimoire.players_list:
            if player.true_role == "杀手":
                string = f"你是 玩家{player.player_index} 杀手，你是否选择使用你的刺杀技能， 注意本局游戏你仅有一次刺杀机会(输入 1 使用技能，输入 0 不使用)："
                use_skill = None
                while not isinstance(use_skill, int):
                    try:
                        use_skill = int(input(string))
                        if use_skill != 0 and use_skill != 1:
                            print_to_role(player.true_role, f"请输入 1 使用技能,或输入 0 不使用。")
                    except ValueError:
                        print_to_role(player.true_role, f"请输入 1 使用技能,或输入 0 不使用。")
                player.skill(use_skill)
            if player.true_role == "猩红女郎":
                player.skill()

    def check_win(self):
        alive_in_game = [i for i in grimoire.players_list if i.is_alive]
        alive_register_in_game = [i.role_for_register for i in grimoire.players_list if i.is_alive]
        good_guys_win = False
        bad_guys_win = False
        # 场上不存在恶魔，且没有办法立即生成一个新的恶魔，即好人方获胜
        if "小恶魔" not in alive_register_in_game:
            good_guys_win = True
        # 如果好人方全部死亡，则恶魔方胜利。
        alive_good_guys = [i for i in grimoire.players_list if i.is_good_guy and i.is_alive]
        if not alive_good_guys:
            bad_guys_win = True
        # 如只剩2名玩家，恶魔在场，则恶魔方直接胜利。
        elif len(alive_in_game) <= 2 and "小恶魔" in alive_register_in_game:
            bad_guys_win = True
        return good_guys_win, bad_guys_win


storyteller = Storyteller()
