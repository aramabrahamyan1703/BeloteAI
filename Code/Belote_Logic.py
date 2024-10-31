import itertools
import random
#For color, but since the engine prints color char by char it seems difficult so idk
#from colorama import init as colorama_init
#from colorama import Fore
#from colorama import Style
SCREEN_SIZE = (150, 40)


HIDDEN_CARD_LEFT_RIGHT = """\
┌──────────┐
│░░░░░░░░░░│
│░░░░░░░░░░│
└──────────┘
"""

HIDDEN_CARD_TOP = """\
┌─────┐
│░░░░░│
│░░░░░│
│░░░░░│
│░░░░░│
│░░░░░│
└─────┘
"""


CARD = """\
┌─────────┐
│{}       │
│         │
│         │
│    {}   │
│         │
│         │
│       {}│
└─────────┘
""".format('{rank: <2}', '{suit: <2}',  '{rank: >2}')

def ascii_version_of_card(card):
    suit_to_symbol = ["♡", '♤', '♧', '♢']
    rank_to_char = ["T", "K", "D", "V", "10", "9", "8", "7"]
    return CARD.format(rank=rank_to_char[card[0]], suit=suit_to_symbol[card[1]])

def ascii_version_of_hidden_card(left_right):
    return HIDDEN_CARD_LEFT_RIGHT if left_right else HIDDEN_CARD_TOP
    
class Cards:
    def __init__(self) -> None:
        self.standard_cards: list[int] = [11, 4, 3, 2, 10, 0, 0, 0] # T, K, D, V, 10, 9, 8, 7
        self.trump_cards: list[int] = [11, 4, 3, 20, 10, 14, 0, 0]
        self.no_trump_cards: list[int] = [19, 4, 3, 2, 10, 0, 0, 0]
        self.trump_suit: int = 0  # 0 - Hearts, 1 - Spades, 2 - Clubs, 3 - Diamonds
        self.deck = None
        
    def who_takes(self, cards: list[list[int]]):
        first_suit = cards[0][0] # [[Suit, Value]] 
        
        curr_max_first_suit = (0, 0)  #(Index, Value)
        curr_max_trump_suit = None 
        
        for index in range(len(cards)):
            if cards[index][0] == first_suit:
                if cards[index][1] > curr_max_first_suit[1]:
                    curr_max_first_suit = index, cards[index][1]
            
            if cards[index][0] == self.trump_cards:
                if cards[index][1] > curr_max_first_suit[1]:
                    curr_max_trump_suit = index, cards[index][1]
        
        return curr_max_trump_suit if curr_max_trump_suit else curr_max_first_suit
    
    def set_trump(self, suit: int) -> None:
        self.trump_suit = suit
    
    def create_deck(self):
        vals = [0, 1, 2, 3, 4, 5, 6, 7] # T, K, D, V, 10, 9, 8, 7
        suits = [0, 1, 2, 3] # 0 - Hearts, 1 - Spades, 2 - Clubs, 3 - Diamonds
        deck = list(itertools.product(vals, suits))
        random.shuffle(deck)
        self.deck = deck
        
