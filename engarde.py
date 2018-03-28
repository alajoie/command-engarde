import time
import card
import piste
import player
import random
from random import shuffle


deck = []
discards = []

duelLength = 5

cls = chr(27)+"[H" + chr(27) + "[J"  

def init_deck():
    return [card.Card(value) for value in range(1,6) for x in range(1,6)]
    
def init_discards():
    return [["[1]"],["[2]"],["[3]"],["[4]"],["[5]"]]
            
def splash(splash_file):
    lines = [line.rstrip('\n') for line in open(str(splash_file))]
    for line in lines:
        print(line)
    print("Press Enter to begin En Garde!")
    wait = input()

def set_game_length():
    print(cls)
    lengthEntered = False
    while(lengthEntered != True):
        print("How long of a duel would you like? 1, 3, or 5 hits against:")
        duelLength = input()
        try:
            duelLength = int(duelLength)
        except ValueError:
            print("That is not a proper length or ")
            lengthEntered = False
        if(duelLength == 1):
            print("To first Blood!")
            print("... summoning the seconds .", end="")
            time.sleep(1)
            print(".", end="")
            time.sleep(1)
            print(".")
            time.sleep(1)
            lengthEntered = True
            break
        elif(duelLength == 3):
            print("Ah... a short duel to pass the time ...")
            print("... calling the leeches .", end="")
            time.sleep(1)
            print(".", end="")
            time.sleep(1)
            print(".")
            time.sleep(1)
            lengthEntered = True
            break
        elif(duelLength == 5):
            print("Ahhhh! nothing like a duel to get the blood flowing!")
            print("... the dueling grounds are waiting .", end="")
            time.sleep(1)
            print(".", end="")
            time.sleep(1)
            print(".")
            time.sleep(1)
            lengthEntered = True
            break
        else:
            print("Please try a different length ...")
            lengthEntered = False
    return duelLength

def display_hits(player1, player2):
    p1Hits = ""
    p2Hits = ""
    for hit in range(player1.hits):
        p1Hits += "\033[31m"+"X "+"\033[37m"
    for hit in range(player2.hits):
        p2Hits += "\033[31m"+"X "+"\033[37m"
    print("Hits Against -> Player:" + p1Hits +"    Computer:" + p2Hits)

def display_board(player1, player2, piste):
    print(cls)
    display_hits(player1,player2)
    print("Cards Remaining: " + str(len(deck)))
    print(piste)

def show(deck):
    for card in deck:
        print(str(card.value) + ' ', end='')
    print()

def show_discards(discards):
    for row in discards:
        d_row = ""
        for cardValue in row:
            d_row += cardValue
        print(d_row)

def show_hand(player):
    print("Your hand contains: ")
    player.show_hand()

def init_deal(deck, p1, p2):
    p1.hand = []
    p2.hand = []
    for i in range(0,5):
        p1.hand.append(deck.pop())
        p2.hand.append(deck.pop())

def can_advance(piste, card):
    return piste.range > card.value

def can_lunge(piste, card):
    return piste.range == card.value

def can_retreat(player, card):
    return player.range_to_end >= card.value

def show_valid_moves(player, card, piste):
    display = "You may "
    if(can_retreat(player, card)):
        display += "[R]etreat, "
    if(can_lunge(piste, card)):
        display += "[L]unge, "
    if(can_advance(piste, card)):
        display += "[A]dvance, "
    display += "or r[E]place the card to start again."
    return display

def discard(card, discards):
    row_index = card.value - 1
    discards[row_index].append("{+}")

def select_movement_card(player):
    cardFound = False
    m_card = None
    while(cardFound != True):
        print("Select a movement card: ")
        m_card = input()
        try:    
            m_card = int(m_card)
        except ValueError:
            print("That was not a valid card value or ")
            cardFound = False
        for card in player.hand:
            if(card.value == m_card):
                m_card = card
                player.hand.remove(card)
                cardFound = True
                break
        if(cardFound != True):
            print("You do not have a card with that value.")
    return m_card

def select_action(player, opponent, card, piste, discards, deck):
    actionSelected = False
    while(actionSelected != True):
        print(show_valid_moves(player, card, piste))
        action = input()
        if(action == 'L' and can_lunge(piste, card)):
            opponent.token = "\033[31m"+"X"
            piste.update()
            piste.range = 0
            opponent.hit()
            display_board(player, opponent, piste)
            print("Touche!")
            actionSelected = True
            return True
        elif(action == 'A' and can_advance(piste, card)):
            player.advance(card.value)
            piste.update()
            discard(card, discards)
            try:
                player.hand.append(deck.pop())
            except IndexError:
                print()
            actionSelected = True
            return True
        elif(action == 'R' and can_retreat(player, card)):
            player.retreat(card.value)
            piste.update()
            discard(card, discards)
            try:
                player.hand.append(deck.pop())
            except IndexError:
                print()
            actionSelected = True
            return True
        elif(action == 'E'):
            player.hand.append(card)
            actionSelected = True
            return False
        else:
            print("That is not a valid action. Please try again.")
    return False

def computerTurn(player, opponent, piste, discards, deck):
    display_board(opponent, player, piste)
    show_discards(discards)
    print("Computer Turn ...")
    print("... assessing the terrain ...")
    time.sleep(2)
    print("... determining safest move ...")
    time.sleep(2)
    for card in player.hand:
        if(card.value == piste.range):
            opponent.token = "\033[31m" + "X"
            piste.update()
            opponent.hit()
            piste.range = 0
            display_board(opponent, player, piste)
            print("Touche!")
            return False
    for card in player.hand:
        if(can_advance(piste, card) and (piste.range - card.value) > 5):
            player.advance(card.value)
            piste.update()
            player.hand.remove(card)
            discard(card, discards)
            try:
                player.hand.append(deck.pop())
            except IndexError:
                print()
            return True
    for card in player.hand:
        if(can_retreat(player, card)):
            player.retreat(card.value)
            piste.update()
            player.hand.remove(card)
            discard(card, discards)
            try:
                player.hand.append(deck.pop())
            except IndexError:
                print()
            return True
    for card in player.hand:
        if(can_advance(piste, card)):
            player.advance(card.value)
            piste.update()
            player.hand.remove(card)
            discard(card, discards)
            try:
                player.hand.append(deck.pop())
            except IndexError:
                print()
            return True

def personTurn(player, opponent, piste, discards, deck):
    turnOver = False
    while(turnOver != True):
        display_board(player, opponent, piste)
        show_discards(discards)
        print()
        show_hand(player)
        print()
        m_choice = select_movement_card(player)
        turnOver = select_action(player, opponent, m_choice, piste, discards, deck)

    if(piste.range == 0):
        return False
    return True

def lastAttack(player, computer, piste, deck):
    display_board(player, computer, piste)
    show_discards(discards)
    if(len(deck) == 0):
        pRange = abs(player.position - (len(piste.spaces)/2))
        cRange = abs(computer.position - (len(piste.spaces)/2))
        if(pRange < cRange): 
            computer.token = "\033[31m" + "X"
            piste.update()
            computer.hit()
            piste.range = 0
            display_board(player, computer, piste)
            print("Computer loses by position")
        else:
            player.token = "\033[31m" + "X"
            piste.update()
            player.hit()
            piste.range = 0
            display_board(player, computer, piste)
            print("Player loses by position")
        return False

    return True


player1 = player.Player("P")
player2 = player.Player("C")

piste = piste.Piste(player1, player2)

print(cls)
splash('musk1.asc')

duelLength = set_game_length()

print(cls)

fenceOn = True
boutCount = 1
while(fenceOn):
    
    keepBouting = True
    if(player1.hits == duelLength or player2.hits == duelLength):
        keepBouting = False
        fenceOn = False
    else:
        deck = init_deck()
        discards = init_discards()
        shuffle(deck)
        player1.token = "P"
        player2.token = "C"
        init_deal(deck, player1, player2)
        piste.reset(player1, player2)
        print(cls)
        print("\n\n\n\n\n")
        print("Bout: " + str(boutCount) + " starting... En Garde!")
        print("(Press ENTER)")
        wait = input()

    while(keepBouting):
        if(keepBouting):
            keepBouting = personTurn(player1, player2, piste, discards, deck)
        if(keepBouting):
            keepBouting = computerTurn(player2, player1, piste, discards, deck)
        if(keepBouting):
            keepBouting = lastAttack(player1, player2, piste, deck)
    
    print("Press Enter to Continue")
    wait = input()        
    boutCount += 1

print("Game Over!")
