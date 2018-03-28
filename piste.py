import player

class Piste:
    LEFTEND = 0
    RIGHTEND = 22

    def __init__(self, player1, player2):
        player1.side = "L"
        self.left_player = player1
        player2.side = "R"
        self.right_player = player2
        self.range = 0
        self.init_player_positions()
        self.spaces = []
        self.update()

    def reset(self, player1, player2):
        player1.side = "L"
        self.left_player = player1
        player2.side = "R"
        self.right_player = player2
        self.range = 0
        self.init_player_positions()
        self.spaces = []
        self.update()

    def __str__(self):
        display = ""
        for index, space in enumerate(self.spaces):
            if(index == 11):
                display += "\033[1;33m" + "[" + str(space) + "\033[1;33m" + "]"
            else:    
                display += "\033[0;37m" + "[" + str(space) + "\033[0;37m" + "]"
        display += "\n"
        display += "Range: " + str(self.range)
        return display

    def init_player_positions(self):
        self.left_player.position = self.LEFTEND
        self.right_player.position = self.RIGHTEND
        self.update_player_ranges()
 
    def update_player_ranges(self):
        self.left_player.range_to_end = self.left_player.position - self.LEFTEND
        self.right_player.range_to_end = self.RIGHTEND - self.right_player.position
        self.range = self.right_player.position - self.left_player.position

    def update(self):
        self.spaces = [' ' for i in range(1,24)]
        self.spaces[self.left_player.position] = self.left_player
        self.spaces[self.right_player.position] = self.right_player
        self.update_player_ranges()

