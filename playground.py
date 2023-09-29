import random
from random import sample
from random import choice
import botc
from botc.core.roles import Washerwoman
from botc.core.roles import Librarian
from botc.core.roles import Investigator
from botc.core.roles import Cook
from botc.core.roles import Empath

from botc.core.nights import first_night
from botc.core.nights import other_nights

role_list = [Washerwoman(), Librarian(), Investigator(), Cook(), Empath()]

players_num = 2


alive_player_list = []
players_list = sample(role_list, players_num)

for i in range(players_num):
    players_list[i].player_index = i + 1
    players_list[i].players_list = players_list

print(players_list[1].players_list)


def main():
    is_first_night = True
    is_night = True
    if is_night:
        is_night = False
        if is_first_night:
            is_first_night = False
            first_night()
        else:
            other_nights()




