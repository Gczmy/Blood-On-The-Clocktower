from random import sample
import botc.core.roles as roles


def create_players_list(players_num):
    if players_num == 5:
        # 村民3人，外乡人0，爪牙1，恶魔1
        players_list = sample(roles.villager_list, 3) + sample(roles.outlander_list, 0) + sample(roles.minion_list,
                                                                                                 1) + sample(
            roles.demon_list, 1)
    elif players_num == 6:
        # 村民3人，外乡人1，爪牙1，恶魔1
        players_list = sample(roles.villager_list, 3) + sample(roles.outlander_list, 1) + sample(roles.minion_list,
                                                                                                 1) + sample(
            roles.demon_list, 1)
    elif players_num == 7:
        # 村民5人，外乡人0，爪牙1，恶魔1
        players_list = sample(roles.villager_list, 5) + sample(roles.outlander_list, 0) + sample(roles.minion_list,
                                                                                                 1) + sample(
            roles.demon_list, 1)
    elif players_num == 8:
        # 村民5人，外乡人1，爪牙1，恶魔1
        players_list = sample(roles.villager_list, 5) + sample(roles.outlander_list, 1) + sample(roles.minion_list, 1) + sample(roles.demon_list, 1)
    elif players_num == 9:
        # 村民5人，外乡人2，爪牙1，恶魔1
        players_list = sample(roles.villager_list, 5) + sample(roles.outlander_list, 2) + sample(roles.minion_list,
                                                                                                 1) + sample(
            roles.demon_list, 1)
    elif players_num == 10:
        # 村民7人，外乡人0，爪牙2，恶魔1
        players_list = sample(roles.villager_list, 7) + sample(roles.outlander_list, 0) + sample(roles.minion_list,
                                                                                                 2) + sample(
            roles.demon_list, 1)
    elif players_num == 11:
        # 村民7人，外乡人1，爪牙2，恶魔1
        players_list = sample(roles.villager_list, 7) + sample(roles.outlander_list, 1) + sample(roles.minion_list,
                                                                                                 2) + sample(
            roles.demon_list, 1)
    elif players_num == 12:
        # 村民7人，外乡人2，爪牙2，恶魔1
        players_list = sample(roles.villager_list, 7) + sample(roles.outlander_list, 2) + sample(roles.minion_list,
                                                                                                 2) + sample(
            roles.demon_list, 1)
    elif players_num == 13:
        # 村民9人，外乡人0，爪牙3，恶魔1
        players_list = sample(roles.villager_list, 9) + sample(roles.outlander_list, 0) + sample(roles.minion_list,
                                                                                                 3) + sample(
            roles.demon_list, 1)
    elif players_num == 14:
        # 村民9人，外乡人1，爪牙3，恶魔1
        players_list = sample(roles.villager_list, 9) + sample(roles.outlander_list, 1) + sample(roles.minion_list,
                                                                                                 3) + sample(
            roles.demon_list, 1)
    elif players_num == 15:
        # 村民9人，外乡人2，爪牙3，恶魔1
        players_list = sample(roles.villager_list, 9) + sample(roles.outlander_list, 2) + sample(roles.minion_list,
                                                                                                 3) + sample(
            roles.demon_list, 1)
    else:
        raise ValueError("玩家人数必须在5~15人之间！")

    for i in players_list:
        if i.true_role == "男爵":
            players_list = roles.Baron().passive_skill(players_list)
    for i in range(players_num):
        players_list[i].player_index = i + 1
        players_list[i].players_list = players_list
    return players_list
