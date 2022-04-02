#!/usr/local/bin/python3
# Written By David Theriault
# 4/1/2022

from Deck import Deck

class WarDeck(Deck):
    def __init__(self, decks=1, jokers=0, cards=None):
        super().__init__(decks, jokers)
        if(cards):
            self.deck = cards
        self.winnings = []
       
    def nextCard(self):
        card=None
        if(len(self.deck)):
            card = self.deck.pop()
        elif(len(self.winnings)):
            self.deck = self.winnings
            self.winnings = []
            self.shuffle()
            card = self.deck.pop()
        return card

    def cardCount(self):
        return len(self.deck) + len(self.winnings)

    def addWinners(self, winnings):
        for winner in winnings:
            self.winnings.append(winner)

    def __str__(self):
        msg = super().__str__()
        msg += "winnings:\n"
        count = 1
        for card in self.winnings:
            msg += "%2d: %s\n" % (count, str(card))
            count += 1
        return msg

class War:
    def __init__(self, decks=1, jokers=0, player_1_cards=None, player_2_war_deck=None):
        p1_deck = WarDeck(decks=decks, jokers=jokers)
        p1_deck.shuffle()
        mid_point = player_1_cards or int(len(p1_deck.deck) / 2)
        p2_deck = player_2_war_deck or WarDeck(decks=0, jokers=0, cards=p1_deck.deck[mid_point:])
        p1_deck.deck = p1_deck.deck[:mid_point]
        self.p1_deck = p1_deck
        self.p2_deck = p2_deck

        # stats
        self.round = 0
        self.wars  = 0
        self.max_war_depth = 0
        self.winner = 0

    
    def __str__(self):
        msg = "player 1 deck:\n" + str(self.p1_deck)
        msg += "\nplayer 2 deck:\n" + str(self.p2_deck)
        return msg

    # war match
    def war(self, cards_in_war, war_round=1):
        self.wars += 1
        if(war_round > self.max_war_depth):
            self.max_war_depth = war_round

        # want 4 more card, do players have that many left?
        p1_cards_left = self.p1_deck.cardCount()
        p2_cards_left = self.p2_deck.cardCount()
        if(p1_cards_left < 1): 
            print("Player 1 does not have enough cards to continue");
            return
        if(p2_cards_left < 1): 
            print("Player 2 does not have enough cards to continue");
            return
        min_cards_left = min(p1_cards_left, p2_cards_left)
        # 3 down, 1 up
        war_card_number = 4
        if(min_cards_left < war_card_number):
            #print("not enough cards for full war, player 1 has %d, player 2 has:%d" % (p1_cards_left, p2_cards_left))
            war_card_number = min_cards_left

        for ante in range(1, war_card_number+1):
            p1_war_card = self.p1_deck.nextCard()
            p2_war_card = self.p2_deck.nextCard()
            cards_in_war.append(p1_war_card)
            cards_in_war.append(p2_war_card)
            if(ante < war_card_number):
                pass
                #print("\t\t%d:%s - %s" %(ante + ((war_round-1) * 3), p1_war_card, p2_war_card))


        if(p1_war_card > p2_war_card):
            #print("\t\tPlayer 1 wins war %s  > %s" % (p1_war_card, p2_war_card))
            self.p1_deck.addWinners(cards_in_war)
        elif(p1_war_card < p2_war_card):
            #print("\t\tPlayer 2 wins war %s  < %s" % (p1_war_card, p2_war_card))
            self.p2_deck.addWinners(cards_in_war)
        else:
            war_round += 1
            #print("\t\tWar Round %d! %s  = %s" % (war_round, p1_war_card, p2_war_card))
            self.war(cards_in_war, war_round)
            

    def match(self):
        self.round += 1
        p1_card = self.p1_deck.nextCard()
        p2_card = self.p2_deck.nextCard()
        if(p1_card > p2_card):
            #print("R:%3d\tP1 wins %s  > %s" % (self.round, p1_card, p2_card))
            self.p1_deck.addWinners([p1_card, p2_card])
        elif(p1_card < p2_card):
            #print("R:%3d\tP2 wins %s  < %s" % (self.round, p1_card, p2_card))
            self.p2_deck.addWinners([p1_card, p2_card])
        else:
            #print("R:%3d\tWAR %s  = %s" % (self.round, p1_card, p2_card))
            self.war([p1_card, p2_card], 1)
        # debug
        #print("ending player1:\n%s\nending player2:\n%s" % (self.p1_deck, self.p2_deck))

    def play(self):
        while(self.p1_deck.cardCount() > 0 and self.p2_deck.cardCount() > 0):
            self.match()
        self.winner = 1
        if(self.p2_deck.cardCount()):
            self.winner = 2
        print("\nPlayer %d won after %3d rounds\nThere were %d wars with a max of %d war levels" % (self.winner, self.round, self.wars, self.max_war_depth))

class Stats:
    def __init__(self, runs=1000, decks=1, jokers=0, player_1_cards=None ):
        self.p1_wins = 0
        self.p2_wins = 0
        self.total_rounds = 0
        self.max_rounds = 0
        self.min_rounds = 0
        self.total_wars = 0
        self.min_wars = 0
        self.max_wars = 0
        self.max_war_depth = 0
        self.runs = runs
        self.player_1_cards=player_1_cards
        self.jokers=jokers
        self.decks=decks

    def simulation(self, joker_test=False):
        runs = self.runs
        for sim in range(runs):
            player_2_war_deck = None
            if(joker_test):
                player_2_war_deck = WarDeck(decks=0, jokers=1)
            war = War(self.decks, self.jokers, self.player_1_cards, player_2_war_deck)
            #print(war)
            war.play()
            # war stuff
            if(war.winner == 1):
                self.p1_wins += 1
            else:
                self.p2_wins += 1

            if(war.round < self.min_rounds or not self.min_rounds):
                self.min_rounds = war.round
            if(war.round > self.max_rounds):
                self.max_rounds = war.round

            self.total_rounds += war.round
            
            if(war.wars < self.min_wars or not self.min_wars):
                self.min_wars = war.wars
            if(war.wars > self.max_wars):
                self.max_wars = war.wars

            self.total_wars += war.wars
            
            if(war.max_war_depth > self.max_war_depth):
                self.max_war_depth = war.max_war_depth

        # calc averages
        p1_win_ratio = self.p1_wins / runs * 100
        avg_rounds = self.total_rounds / runs
        avg_wars = self.total_wars / runs
        # print final results
        print("\n\n%d Simulations complete\nPlayer 1 won %.3f%%" % (runs, p1_win_ratio))
        print("Avg rounds: %.3f, min rounds:%d, max rounds:%d" % (avg_rounds, self.min_rounds, self.max_rounds))
        print("Avg wars: %.3f, min wars:%d, max wars:%d" % (avg_wars, self.min_wars, self.max_wars))
        print("Max war levels: %d" % self.max_war_depth)
        

if __name__ == '__main__':
    # General Simulation
    stat = Stats(runs=1000)
    stat.simulation(joker_test=False)
    # Joker Test Simulation
    stat = Stats(runs=1000, player_1_cards=52)
    stat.simulation(joker_test=True)

