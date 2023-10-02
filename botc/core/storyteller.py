from collections import Counter
import botc.core.backend as backend
from botc.core.print import print_to_all
from botc.core.print import print_to_role
from botc.core.print import clear_all_print_file
from botc.core.print import print_to_prompt
from botc.core.print import print_to_backend


class Storyteller:
    def __init__(self):
        self.players_list = None
        self.butler_to_follow = None
        self.monk_to_protect = None
        self.imp_to_kill = None
        self.player_to_vote = None
        self.execute_player = None
        self.killed_last_night = None
        self.player_vote_list = []

    def check_kill_in_night(self):
        if self.imp_to_kill is not None:
            if self.imp_to_kill.true_role == "小恶魔":
                # ToDo 小恶魔选择杀死自己
                pass
            elif self.monk_to_protect != self.imp_to_kill:
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

    def __check_butler_follow(self, alive_list):
        alive_role_list = [i.true_role for i in alive_list]
        master_role = None
        master_has_voted = None
        butler_index = None
        for i in self.players_list:
            if i.true_role == "管家":
                butler_index = i.player_index
        if self.butler_to_follow is not None:
            master_role = self.butler_to_follow.true_role  # 主人的身份
            master_has_voted = None
            if self.players_list[butler_index].is_alive:
                # 如果管家活着，将管家放到列表的最后，确保管家在主人之后投票
                alive_role_list.remove("管家")
                alive_role_list.append("管家")
        return alive_role_list, butler_index, master_role, master_has_voted

    def vote_to_execute(self):
        print("投票开始")
        alive_list = [i for i in self.players_list if i.is_alive]
        butler = None
        for player in alive_list:
            if player.true_role == "管家":
                # 如果管家活着，将管家放到列表的最后，确保管家在主人之后投票
                butler = player
                continue
            player.vote()
        if butler is not None:
            butler.vote()
        # 唱票
        print_to_all("投票结束")
        vote_counts = Counter(self.player_vote_list)
        most_common_vote = vote_counts.most_common(1)
        if len(vote_counts.values()) > 1:
            most_common_vote = vote_counts.most_common(2)
            if most_common_vote[0][1] == most_common_vote[1][1]:
                backend.info.append(f"玩家平票，没有玩家被处决")
                print_to_all(f"玩家平票，没有玩家被处决")
                execute_player = None
            else:
                execute_player = most_common_vote[0][0]
                print_to_all(f"玩家{execute_player} 票数最多，被处决")
                execute_player = [i for i in self.players_list if i.player_index == execute_player][0]
                backend.info.append(f"玩家{execute_player.player_index} {execute_player.true_role} 票数最多，被处决")
                execute_player.dead()
        elif not most_common_vote:
            backend.info.append(f"所有玩家弃票，没有玩家被处决")
            print_to_all(f"所有玩家弃票，没有玩家被处决")
            execute_player = None
        else:
            execute_player = most_common_vote[0][0]
            print_to_all(f"玩家{execute_player} 票数最多，被处决")
            execute_player = [i for i in self.players_list if i.player_index == execute_player][0]
            backend.info.append(f"玩家{execute_player.player_index} {execute_player.true_role} 票数最多，被处决")
            execute_player.dead()

        # Todo:统计票数环节可以让玩家们退票，如果主人退票，管家也必须退票
        self.player_vote_list = []
        self.player_to_vote = None

    def check_win(self):
        alive_in_game = [i for i in self.players_list if i.is_alive]
        alive_roles_in_game = [i.true_role for i in self.players_list if i.is_alive]
        good_guys_win = False
        bad_guys_win = False
        # 场上不存在恶魔，且没有办法立即生成一个新的恶魔，即好人方获胜
        if "小恶魔" not in alive_roles_in_game:
            good_guys_win = True
        # 如果好人方全部死亡，则恶魔方胜利。
        alive_good_guys = [i for i in self.players_list if i.is_good_guy and i.is_alive]
        if not alive_good_guys:
            bad_guys_win = True
        # 如只剩2名玩家，恶魔在场，则恶魔方直接胜利。
        elif len(alive_in_game) <= 2 and "小恶魔" in alive_roles_in_game:
            bad_guys_win = True
        return good_guys_win, bad_guys_win


storyteller = Storyteller()
