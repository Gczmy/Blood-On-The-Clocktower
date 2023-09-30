player_to_vote = None
player_to_protect = None
player_to_kill = None


def storyteller():
    if player_to_kill is not None and player_to_protect != player_to_kill:
        player_to_kill.dead()

    if player_to_vote is not None:
        pass
