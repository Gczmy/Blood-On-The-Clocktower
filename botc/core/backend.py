import random
from random import sample
from random import choice
from botc.core.print import print_to_backend

info = []


def print_all_info():
    for i in info:
        print_to_backend(i)


def print_last_info():
    print(info[-1])
