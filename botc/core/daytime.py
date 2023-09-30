def check_alive(players_list):
    alive_list = [i for i in players_list if i.is_alive]
    print("目前还存活的玩家编号为：", [i.player_index for i in alive_list])
    return alive_list
