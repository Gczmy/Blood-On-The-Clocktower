from collections import Counter
import botc.core.backend as backend
from botc.core.print import print_to_all
from botc.core.print import print_to_role
from botc.core.print import clear_all_print_file
from botc.core.print import print_to_prompt


class Storyteller:
    def __init__(self):
        self.players_list = None
        self.player_to_follow = None
        self.player_to_protect = None
        self.player_to_kill = None
        self.player_to_vote = None
        self.execute_player = None

    def check_kill(self):
        if self.player_to_kill is not None:
            if self.player_to_kill.true_role == "小恶魔":
                # 小恶魔选择杀死自己
                pass
            elif self.player_to_protect != self.player_to_kill:
                # 小恶魔选择杀死的人和僧侣选择保护的人不是同一个人, 则被小恶魔选择杀死的人死亡
                self.player_to_kill.dead()

    def __check_butler_follow(self, alive_list):
        alive_role_list = [i.true_role for i in alive_list]
        master_role = None
        master_has_voted = None
        butler_index = None
        for i in self.players_list:
            if i.true_role == "管家":
                butler_index = i.player_index
        if self.player_to_follow is not None:
            master_role = self.player_to_follow.true_role  # 主人的身份
            master_has_voted = None
            if self.players_list[butler_index].is_alive:
                # 如果管家活着，将管家放到列表的最后，确保管家在主人之后投票
                alive_role_list.remove("管家")
                alive_role_list.append("管家")
        return alive_role_list, butler_index, master_role, master_has_voted

    def __vote_input(self, current_role, alive_player_index_list, string):
        player_input = None
        while not isinstance(player_input, int) or not (player_input in alive_player_index_list or player_input == 0):
            try:
                player_input = int(input(string + str(alive_player_index_list)))
                if player_input < 0 or player_input > len(alive_player_index_list):
                    print_to_role(current_role, f"请输入玩家编号{alive_player_index_list},或输入 0 弃票。")
            except ValueError:
                print_to_role(current_role, f"请输入玩家编号{alive_player_index_list},或输入 0 弃票。")
        return player_input

    def vote_to_execute(self):
        print("投票开始")
        alive_list = [i for i in self.players_list if i.is_alive]
        alive_player_index_list = [i.player_index for i in alive_list]

        alive_role_list, butler_index, master_role, master_has_voted = self.__check_butler_follow(alive_list)
        player_vote_list = []

        for player in alive_list:
            # current_player = [i.player_index for i in alive_list if i.true_role == current_role][0]
            if player.true_role == "管家":
                # 管家玩家投票
                if player.toxic:
                    player_to_execute = self.__vote_input(player.true_role, alive_player_index_list,
                                                          f"你是{player.player_index} {player.role_for_register}, 请输入玩家编号以投票处决一位玩家(输入 0 视为弃票)：")
                    if player_to_execute == 0:
                        # 玩家弃票
                        backend.info.append(f"玩家{player.player_index} 选择弃票")
                        print_to_all(f"玩家{player.player_index} 选择弃票")
                    else:
                        player_vote_list.append(player_to_execute)
                        print_to_all(f"玩家{player.player_index} 选择投票给 玩家{player_to_execute}")
                        player_to_execute = [i for i in self.players_list if i.player_index == player_to_execute][0]
                        backend.info.append(
                            f"玩家{player.player_index} {player.true_role} 选择投票给 玩家{player_to_execute.player_index} {player_to_execute.true_role}")
                else:
                    if master_has_voted is not None:
                        # 主人投了票
                        player_to_execute = self.__vote_input(player.true_role, alive_player_index_list,
                                                              f"你是玩家{player.player_index} {player.role_for_register}, "
                                                              f"你昨晚选择的主人选择投票给 玩家{player_to_execute.player_index}, "
                                                              f"请输入玩家编号以投票处决一位玩家(输入 0 视为弃票)：")
                        if player_to_execute == 0:
                            # 玩家弃票
                            backend.info.append(f"玩家{player.player_index} 选择弃票")
                            print_to_all(f"玩家{player.player_index} 选择弃票")
                        else:
                            player_vote_list.append(player_to_execute)
                            print_to_all(f"玩家{player.player_index} 选择投票给 玩家{player_to_execute}")
                            player_to_execute = [i for i in self.players_list if i.player_index == player_to_execute][0]
                            backend.info.append(
                                f"玩家{player.player_index} {player.true_role} 选择投票给 玩家{player_to_execute.player_index} {player_to_execute.true_role}")
                    else:
                        # 主人没投票
                        player_to_execute = 0
                        backend.info.append(f"玩家{player.player_index} 选择弃票")
                        print_to_all(f"玩家{player.player_index} 选择弃票")
                        backend.info.append(
                            f"玩家{player.player_index} 管家, 由于昨晚他选择的主人弃票，因此他也无法投票，视为直接弃票")
                        player.info = f"你是 玩家{player.player_index} 管家, 由于昨晚你选择的主人弃票，因此你也无法投票，视为直接弃票"
                        print_to_role(player.true_role, player.info)
            else:
                # 非管家玩家投票
                player_to_execute = self.__vote_input(player.true_role, alive_player_index_list,
                                                      f"你是{player.player_index} {player.role_for_register}, 请输入玩家编号以投票处决一位玩家(输入 0 视为弃票)：")

                if player_to_execute == 0:
                    # 玩家弃票
                    backend.info.append(f"玩家{player.player_index} 选择弃票")
                    print_to_all(f"玩家{player.player_index} 选择弃票")
                else:
                    # 玩家投了票
                    if "管家" in alive_role_list:
                        if player.true_role == master_role:
                            master_has_voted = player_to_execute
                    player_vote_list.append(player_to_execute)
                    print_to_all(f"玩家{player.player_index} 选择投票给 玩家{player_to_execute}")
                    player_to_execute = [i for i in self.players_list if i.player_index == player_to_execute][0]
                    backend.info.append(f"玩家{player.player_index} {player.true_role} 选择投票给 玩家{player_to_execute.player_index} {player_to_execute.true_role}")
        # 唱票
        print_to_all("投票结束")
        vote_counts = Counter(player_vote_list)
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

        self.execute_player = execute_player
        self.player_to_follow = None
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
