class Grimoire:
    def __init__(self):
        self.players_num = None
        self.players_list = None
        self.alive_list = None
        self.before_game = True
        self.is_night = True
        self.is_daytime = False
        self.is_first_night = True
        self.nights_num = 0
        self.backend_info = []


grimoire = Grimoire()
