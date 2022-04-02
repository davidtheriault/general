#!/usr/local/bin/python3
# Written By David Theriault
# 4/1/2022

import random

class Suits:
    def __init__(self):
        self.suits = {\
                      "hearts"   : Heart(),\
                      "clubs"    : Club(),\
                      "diamonds" : Diamond(),\
                      "spades"   : Spade()\
        }

class Suit:
    def __init__(self, name, symbol, color):
        self.name = name
        self.symbol = symbol
        self.color = color

class Spade(Suit):
    def __init__(self):
        super().__init__("Spade", "♠️", "Black")

class Heart(Suit):
    def __init__(self):
        super().__init__("Heart", "❤️", "Red")

class Club(Suit):
    def __init__(self):
        super().__init__("Club", "♣", "Black")

class Diamond(Suit):
    def __init__(self):
        super().__init__("Diamond", "♦️", "Red")


class Card:
    value_map = {}
    for num in range(2,11):
        value_map[str(num)] = num
    value_map['J'] = 11
    value_map['Q'] = 12
    value_map['K'] = 13
    value_map['A'] = 14
    value_map["Joker"] = 15
        
    def __init__(self, Suit, value):
       self.suit=Suit
       self.value=value

    def __str__(self):
        msg = ""
        if(self.value == "Joker"):
            msg = "The Joker %s" % str(self.suit.symbol)
        else:
            msg = "The %s of %s" % (self.value, str(self.suit.symbol))
        return msg

    def __eq__(self, other):
        return self.rank() == other.rank()

    def __ne__(self, other):
        return self.rank() == other.rank()
    
    def __lt__(self, other):
        return self.rank() < other.rank()
    
    def __le__(self, other):
        return self.rank() <= other.rank()

    def __gt__(self, other):
        return self.rank() > other.rank()

    def __ge__(self, other):
        return self.rank() >= other.rank()

    def rank(self):
        return Card.value_map[self.value]

class Deck:
    def __init__(self, decks=1, jokers=0):
        card_vals = ['A', 'K', 'Q', 'J']
        for val in range(2, 11):
            card_vals.append(str(val))

        suits = Suits().suits
        deck = []
        for decks in range(decks):
            for suit in suits.values():
                for val in card_vals:
                    deck.append(Card(suit, val))
        for joker in range(jokers):
            deck.append(Card(Suit("Joker", "🃏", "Joker"), "Joker"))
        self.deck=deck
    
    def __str__(self):
        count = 1
        msg = ""
        for card in self.deck:
            msg += "%2d: %s\n" % (count, str(card))
            count += 1
        return msg

    def shuffle(self):
        random.shuffle(self.deck)

if __name__ == '__main__':
    heart = Heart()
    spade = Spade()
    card_low = Card(heart, '3')
    card_high = Card(spade, 'J')

    #print("card:%s" % str(card_low))
    #print("card:%s" % str(card_high))
    #print("same? %s, < ? %s" % (str(card_low == card_high), str(card_low < card_high)))
    deck = Deck(1,1)
    print("deck?\n%s" % deck)
    deck.shuffle()
    print("deck\n%s" % deck)

