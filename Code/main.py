from playscii import GameManager
from playscii.input import Input
from Belote_Logic import *
from players import *
from auction import *
from enum import Enum
import time
import copy
import random

class GameState(Enum):
    DEALING = "Dealing"
    AUCTIONSUITS = "Auction Suits"
    AUCTIONNUMBER = "Auction Number"
    MAINGAME = "MainGame"
    BOTTURN = "Bot Turn"
    
class PlayersManager(GameManager): # Inherits GameManager
    def __init__(self, cards): 
        super().__init__(SCREEN_SIZE) 
        center = (SCREEN_SIZE[0] // 2 + 4, SCREEN_SIZE[1] // 2 + 4)
        self.main_cards = [] 
        self.suits_prompt = Suits_Prompt((SCREEN_SIZE[0] // 2 - 25, SCREEN_SIZE[1] // 2 + 4))
        self.range_prompt = Range_Prompt((SCREEN_SIZE[0] // 2 - 25, SCREEN_SIZE[1] // 2 + 4))
        
        self.speech_bubble = Speech_Bubble((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        self.speech_bubbles = []
        for _ in range(4):
            self.speech_bubbles.append(copy.deepcopy(self.speech_bubble))
        
        self.game_state = GameState.DEALING.value
        self.start_time = time.time()
        
        self.chosen_suit: list[int] = [None] * 5
        self.auction_start_num = 8
        
        self.turn = 0
        self.noTrumps = False
        self.noTrumpsFinal = False
        
        self.auction_curr_num: list[int] = [self.auction_start_num] * 4
        
        for card in cards[:8]:
            self.main_cards.append(Main_Cards(card, center, main_player=True, left_right=False))

        self.left_bot_cards = []
        for card in cards[8:16]:
            self.left_bot_cards.append(Left_Cards(card, center, main_player=False, left_right=True))
            
        self.right_bot_cards = []
        for card in cards[16:24]:
            self.right_bot_cards.append(Right_Cards(card, center, main_player=False, left_right=True))

        self.top_bot_cards = []
        for card in cards[24:32]:
            self.top_bot_cards.append(Top_Cards(card, center, main_player=False, left_right=False))

        self.set_title("Press q to quit") 
        
    def setup(self): # This is called right before the first update call.
        for card in self.main_cards:
            self.add_object(card) 
        
        for card in self.left_bot_cards:
            self.add_object(card) 
        
        for card in self.right_bot_cards:
            self.add_object(card) 
        
        for card in self.top_bot_cards:
            self.add_object(card) 
            
            
    def update(self): # This is called every frame.
        if Input.get_key_down('q'):
            self.quit() 
            
        if self.game_state == GameState.DEALING.value:
            if time.time() - self.start_time > 3:
                self.game_state = GameState.AUCTIONSUITS.value
        
        if self.game_state == GameState.AUCTIONSUITS.value:
            if not self.suits_prompt in self._GameManager__game_objects:  #Not a good way to do things but it is what it is
                self.add_object(self.suits_prompt)
            self.auction_prompt_manager()
            
        if self.game_state == GameState.AUCTIONNUMBER.value:
            self.auction_prompt_manager()
            
        if self.game_state == GameState.BOTTURN.value:
            self.bot_manager()
    
    
    def bot_manager(self):
        '''
        Test with a random bot TM.
        '''
        
        self.auction_curr_num[self.turn] = random.choice(["Pass", self.auction_start_num + 1, self.auction_start_num + 2])
        self.chosen_suit[self.turn] = random.choice([0,1,2,3,4])
        self.auction_start_num = self.auction_curr_num[self.turn] + 1 if self.auction_curr_num[self.turn] != "Pass" else self.auction_start_num
        suit_to_symbol = ["♡", '♤', '♧', '♢', 'A']
        if self.auction_curr_num[self.turn] == "Pass":
            self.change_turn(self.auction_curr_num[self.turn])
        else:
            if self.noTrumps:
                self.change_turn(f"{suit_to_symbol[self.chosen_suit[self.turn]]} {self.auction_curr_num[self.turn]} CP")
            else:
                self.change_turn(f"{suit_to_symbol[self.chosen_suit[self.turn]]} {self.auction_curr_num[self.turn]}")
        
    
    def change_turn(self, text):
        if self.suits_prompt in self._GameManager__game_objects:
            self._GameManager__game_objects.remove(self.suits_prompt)
            
        if self.range_prompt in self._GameManager__game_objects:
            self._GameManager__game_objects.remove(self.range_prompt)
            
        if self.turn == 3:
            self.game_state = GameState.AUCTIONSUITS.value
        else:
            self.game_state = GameState.BOTTURN.value
        
        if self.speech_bubbles[self.turn] not in self._GameManager__game_objects:
            self.add_object(self.speech_bubbles[self.turn])
    
        self.speech_bubbles[self.turn].set_text(text)
        self.speech_bubbles[self.turn].set_pos(self.turn)
        
        self.turn = (self.turn + 1) % 4
        
        for speach in self.speech_bubbles:
            if speach.text != "Pass":
                return
        
        self.game_state = GameState.MAINGAME.value
            
    def auction_prompt_manager(self):
        def change_promt(suit):
            self.chosen_suit[self.turn] = suit
            if self.suits_prompt in self._GameManager__game_objects:
                self._GameManager__game_objects.remove(self.suits_prompt)
            
            self.auction_curr_num[self.turn] = self.auction_start_num
            self.range_prompt.set_num(f"{self.auction_curr_num[self.turn]} CP" if self.noTrumps else self.auction_curr_num[self.turn]) 
            self.add_object(self.range_prompt)
            self.game_state = GameState.AUCTIONNUMBER.value
            
        
        if self.game_state == GameState.AUCTIONSUITS.value:
            if Input.get_key_down('1'):
                change_promt(0)
            
            if Input.get_key_down('2'):
                change_promt(1)
            
            if Input.get_key_down('3'):
                change_promt(2)
            
            if Input.get_key_down('4'):
                change_promt(3)
            
            if Input.get_key_down('n'):
                change_promt(4)
            
            if Input.get_key_down('p'):
                self.change_turn("Pass")
        
        if self.game_state == GameState.AUCTIONNUMBER.value:
            if Input.get_key_down('left arrow'):
                self.auction_curr_num[self.turn] -= 1 if self.auction_curr_num[self.turn] > self.auction_start_num else 0
                self.range_prompt.set_num(f"{self.auction_curr_num[self.turn]} CP" if self.noTrumps else self.auction_curr_num[self.turn])
                
            if Input.get_key_down('right arrow'):
                self.auction_curr_num[self.turn] += 1 
                self.range_prompt.set_num(f"{self.auction_curr_num[self.turn]} CP" if self.noTrumps else self.auction_curr_num[self.turn])
                
            if Input.get_key_down('c'):
                if not self.noTrumpsFinal:
                    self.noTrumps = not self.noTrumps
                    self.auction_curr_num[self.turn] = 25 if self.auction_start_num < 25 and self.noTrumps else self.auction_start_num
                    self.range_prompt.set_num(f"{self.auction_curr_num[self.turn]} CP" if self.noTrumps else self.auction_curr_num[self.turn])
                
            if Input.get_key_down('esc'):
                self.auction_curr_num[self.turn] = self.auction_start_num
                if self.range_prompt in self._GameManager__game_objects:
                    self._GameManager__game_objects.remove(self.range_prompt)
                self.game_state = GameState.AUCTIONSUITS.value
                
            if Input.get_key_down('p'):
                self.change_turn("Pass")
                
            if Input.get_key_down('d'):
                #TODO: Implement double down logic
                pass
            
            if Input.get_key_down('enter'):
                self.auction_start_num = self.auction_curr_num[self.turn] + 1
                suit_to_symbol = ['♡', '♤', '♧', '♢', 'A']
                if self.noTrumps:
                    self.change_turn(f"{suit_to_symbol[self.chosen_suit[self.turn]]} {self.auction_curr_num[self.turn]} CP")
                else:
                    self.change_turn(f"{suit_to_symbol[self.chosen_suit[self.turn]]} {self.auction_curr_num[self.turn]}")
                
                if self.noTrumps:
                    self.noTrumpsFinal = True

if __name__ == "__main__":
    game = Cards()
    game.create_deck()
    manager = PlayersManager(game.deck)
    manager.start()
    pass