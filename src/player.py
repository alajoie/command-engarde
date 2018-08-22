class Player:
    def __init__(self,token):
        self.token = token
        self.side = ""
        self.position = 0
        self.range_to_end = 0
        self.hand = []
        self.hits = 0

    def __str__(self):
        return self.token

    def show_hand(self):
        display = ""
        for card in self.hand:
            display += "{" + str(card.value) + "}"
        print(display)


    def advance(self, spaces):
        if(self.side == "R"):
            spaces = spaces * -1
        self.position += spaces

    def retreat(self, spaces):
        if(self.side == "L"):
            spaces = spaces * -1
        self.position += spaces

    def hit(self):
        self.hits += 1
