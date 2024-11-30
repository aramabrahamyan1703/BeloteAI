from playscii import GameManager
from playscii.input import Input
from Belote_Logic import *
from players import *
from auction import *
from enum import Enum
from Final_Window import ScoreWindow
import time
import copy
import random
import curses
from Alpha_Beta_Search import Alpha_Beta_Search

curses.initscr()
curses.curs_set(0)

OUR_FINAL_SCORE = 0
THEIR_FINAL_SCORE = 0
CHANGE_WHOSAID = 1

#The game is written with the state machine design pattern (mostly, hopefully)
class GameState(Enum):
    DEALING = "Dealing"
    AUCTIONSUITS = "Auction Suits"
    AUCTIONNUMBER = "Auction Number"
    MAINGAME = "MainGame"
    BOTTURNAUCTION = "Bot Turn"
    PLAYINGCARD = "Playing Card"
    WAITINGFORCARD = "Waiting for card"
    ENDROUND = "Round Ended"
    
class PlayersManager(GameManager): # Inherits GameManager
    def __init__(self, game: Cards): 
        super().__init__(SCREEN_SIZE) 
    
    def setup_players_with_cards(self):
        Main_Cards.index = 0
        self.main_cards: list[Main_Cards] = [] 
        for card in self.cards[:8]:
            self.main_cards.append(Main_Cards(card, self.center, main_player=True, left_right=False))

        Left_Cards.index = 0
        self.left_bot_cards: list[Left_Cards] = []
        for card in self.cards[8:16]:
            self.left_bot_cards.append(Left_Cards(card, self.center, main_player=False, left_right=True))
        
        Right_Cards.index = 0
        self.right_bot_cards: list[Right_Cards] = []
        for card in self.cards[16:24]:
            self.right_bot_cards.append(Right_Cards(card, self.center, main_player=False, left_right=True))

        Top_Cards.index = 0
        self.top_bot_cards: list[Top_Cards] = []
        for card in self.cards[24:32]:
            self.top_bot_cards.append(Top_Cards(card, self.center, main_player=False, left_right=False))
    
    def setup(self): # This is called right before the first update call.
        self.game = game
        self.game.create_deck()
        self.cards = game.deck
        self.center = (SCREEN_SIZE[0] // 2 + 4, SCREEN_SIZE[1] // 2 + 4)
        self.played_cards: list[Main_Cards | Left_Cards | Right_Cards | Top_Cards] = []
        
        self.suits_prompt = Suits_Prompt((SCREEN_SIZE[0] // 2 - 25, SCREEN_SIZE[1] // 2 + 4))
        self.range_prompt = Range_Prompt((SCREEN_SIZE[0] // 2 - 25, SCREEN_SIZE[1] // 2 + 4))
        
        self.speech_bubble = Speech_Bubble((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        self.speech = None #The final decided upon speech bubble 
        self.speech_bubbles = []
        for _ in range(4):
            self.speech_bubbles.append(copy.deepcopy(self.speech_bubble))
        
        self.main_game_starting_player: int = 0
        
        self.first_played_card_suit: int|None = None
        
        self.our_taken_cards: list[Main_Cards | Left_Cards | Right_Cards | Top_Cards] = []
        self.last_took = 0
        
        self.final_window = ScoreWindow()
        self.final_timer = 0
        
        self.game_state = GameState.DEALING.value
        self.start_time = time.time()
        
        self.deal_start_time = time.time()
        self.winner_start_time = time.time()
        
        
        self.chosen_suit: list[int] = [None] * 5
        self.auction_start_num = 8
        
        self.turn = 0
        self.noTrumps = False
        self.noTrumpsFinal = False
        global CHANGE_WHOSAID
        #self.auction_result: list = [None, None, None, None] # KP (0 - no KP, 1 - KP), Suits, Value, Who Called(0 - Us, 1 - Them)
        self.auction_result: list = [0, 1, 8, CHANGE_WHOSAID] # KP (0 - no KP, 1 - KP), Suits, Value, Who Called(0 - Us, 1 - Them)
        self.auction_curr_num: list[int] = [self.auction_start_num] * 4
        self.setup_players_with_cards()

        self.set_title("Press q to quit") 
        
        for card in self.main_cards:
            self.add_object(card) 
        
        for card in self.left_bot_cards:
            self.add_object(card) 
        
        for card in self.right_bot_cards:
            self.add_object(card) 
        
        for card in self.top_bot_cards:
            self.add_object(card) 
                    
    def update(self): #This is called every frame.
        if Input.get_key_down('q'): 
            self.quit() 
            
        if self.game_state == GameState.DEALING.value:
            if time.time() - self.start_time > 3: #3: HERE
                self.game_state = GameState.AUCTIONSUITS.value
        
        if self.game_state == GameState.AUCTIONSUITS.value:
            if not self.suits_prompt in self._GameManager__game_objects:  #Not a good way to do things but it is what it is
                self.add_object(self.suits_prompt)
            self.auction_prompt_manager()
            
        if self.game_state == GameState.AUCTIONNUMBER.value:
            self.auction_prompt_manager()
            
        if self.game_state == GameState.BOTTURNAUCTION.value:
            self.bot_manager()

        if self.game_state == GameState.MAINGAME.value:
            if not self.main_cards and not self.left_bot_cards and not self.right_bot_cards and not self.top_bot_cards:
                score = self.calculate_score()
                self.final_window.set_final_score_text(score)
                self.add_object(self.final_window)
                self.final_timer = time.time()
                self._GameManager__game_objects.remove(self.speech)
                self.winner_start_time = time.time()
                self.game_state = GameState.ENDROUND.value
                return 
            
            if self.turn == 0:
                self.main_game_manager()
            elif self.turn == 1 or self.turn == 3:
                self.random_main_game_bot()
            else:
                self.minimax_main_game_bot()
            pass
        
        if self.game_state == GameState.ENDROUND.value:
            if time.time() - self.final_timer > 5: #Was 5
                self._GameManager__game_objects = []
                flag = False
                
                global OUR_FINAL_SCORE
                global THEIR_FINAL_SCORE
                global CHANGE_WHOSAID
                
                we_won = False
                
                if OUR_FINAL_SCORE > 300 and THEIR_FINAL_SCORE > 300:
                    flag = True
                    if OUR_FINAL_SCORE > THEIR_FINAL_SCORE:
                        self.final_window.set_winner(0)
                        we_won = True
                    else:
                        self.final_window.set_winner(1)
                        
                if OUR_FINAL_SCORE > 300 and THEIR_FINAL_SCORE <= 300:
                    self.final_window.set_winner(0)
                    flag = True
                    we_won = True
                if THEIR_FINAL_SCORE > 300 and OUR_FINAL_SCORE <= 300:
                    self.final_window.set_winner(1)
                    flag = True
                    
                if flag:
                    CHANGE_WHOSAID = (1 + CHANGE_WHOSAID) % 2
                    self.add_object(self.final_window)
                    if time.time() - self.winner_start_time > 8: # Was 8
                        OUR_FINAL_SCORE = 0
                        THEIR_FINAL_SCORE = 0
                        self._GameManager__game_objects = []
                        self.setup()
                else:
                    self.setup()
                return
        
        if self.game_state == GameState.WAITINGFORCARD.value:
            self.clear_card_prompts(self.main_cards)
            if time.time() - self.deal_start_time > 1: #Was 1
                self.game_state = GameState.PLAYINGCARD.value
        
        if self.game_state == GameState.PLAYINGCARD.value:
            self.change_turn_main_game()
    
    def change_turn_main_game(self):
        self.turn = (self.turn + 1) % 4
            
        if len(self.played_cards) == 4:
            cards = []
            for card in self.played_cards:
                cards.append(card.card)
            who_took = game.who_takes(cards)
            self.turn = (self.turn + who_took[0]) % 4 
            for card in self.played_cards:
                card.end_turn(self.turn % 2)
                if self.turn % 2 == 0:
                    self.our_taken_cards.append(card)
            self.played_cards = []
            self.last_took = self.turn % 2
            self.first_played_card_suit = None
        self.game_state = GameState.MAINGAME.value
    
    def calculate_score(self):
        our_total_score = 10 if self.last_took == 0 else 0
        for card in self.our_taken_cards:
            our_total_score += game.get_card_value(card.card)
        their_total_score = 162 - our_total_score
        
        global OUR_FINAL_SCORE
        global THEIR_FINAL_SCORE
        
        #We made the final auction
        if self.auction_result[3] == 0:    
            if our_total_score < self.auction_result[2] * 10:
                THEIR_FINAL_SCORE += 16 + self.auction_result[2]
                return [OUR_FINAL_SCORE, THEIR_FINAL_SCORE]
            OUR_FINAL_SCORE += self.auction_result[2] + int((our_total_score / 10) + 0.4) 
            THEIR_FINAL_SCORE += 16 - int((our_total_score / 10) + 0.4) 
            return [OUR_FINAL_SCORE, THEIR_FINAL_SCORE]
        
        #They made the final auction
        if self.auction_result[3] == 1:     
            if their_total_score < self.auction_result[2] * 10:
                OUR_FINAL_SCORE += 16 + self.auction_result[2]
                return [OUR_FINAL_SCORE, THEIR_FINAL_SCORE]
            THEIR_FINAL_SCORE += self.auction_result[2] + int((their_total_score / 10) + 0.4) 
            OUR_FINAL_SCORE += 16 - int((their_total_score / 10) + 0.4) 
            return [OUR_FINAL_SCORE, THEIR_FINAL_SCORE]
                
    def random_main_game_bot(self):
        valid_cards = self.get_valid_cards(self.first_played_card_suit, self.turn)
        card = random.choice(valid_cards)
        if self.first_played_card_suit == None:
            self.first_played_card_suit = card.card[1]
        self.play_card(card, self.turn)
        self.game_state = GameState.WAITINGFORCARD.value
        
    def minimax_main_game_bot(self):
        card = self.get_player_cards(self.turn)[Alpha_Beta_Search(game, self)]
        if self.first_played_card_suit == None:
            self.first_played_card_suit = card.card[1]
        self.play_card(card, self.turn)
        self.game_state = GameState.WAITINGFORCARD.value
            
    def clear_card_prompts(self, cards):
        for i in cards:
            i.remove_prompt()
    
    def play_card(self, card: int, player):
        cards = []
        
        cards = self.get_player_cards(player)
        
        if player != 0:
            card.show_card()
            
        card.to_play = True
        self.played_cards.append(card)
        if self.turn == 0:
            card.remove_prompt()
        cards.remove(card)
        
        for i, card in enumerate(cards):
            card.arr_index = i
            card.index = i + ((8 - len(cards)) // 2)
            card.inplace = False
        

        self.deal_start_time = time.time()
          
    def get_player_cards(self, player) -> list:
        #Could've been better, but were on a deadline and i have Gen-Ed classes to do.
        if player == 0:
            return self.main_cards
        if player == 1:
            return self.left_bot_cards
        if player == 2:
            return self.top_bot_cards
        if player == 3:
            return self.right_bot_cards
        raise ValueError
    
    def get_valid_cards(self, suit, player):
        #This method uses so many if-s you might as well call it AI.
        cards = self.get_player_cards(player)
        valid_cards = []
        trump_cards_vals: list[int] = [11, 4, 3, 20, 10, 14, 0, 0]
        
        if suit == None:
            return cards
        
        if game.trump_suit == 4:
            #If you have cards of the same suit
            for card_obj in cards:
                if card_obj.card[1] == suit:
                    valid_cards.append(card_obj)         
                    
            #If not, any card         
            return valid_cards if valid_cards else cards
        
        
        temp = []
        for i in self.played_cards:
            temp.append(i.card)
        
        who_takes = game.who_takes(temp)
    
        if suit == game.trump_suit:
            #If you have bigger trump
            max_val = 0
            for card_obj in self.played_cards:
                if card_obj.card[1] == suit:
                    if max_val < trump_cards_vals[card_obj.card[0]]:
                        max_val = trump_cards_vals[card_obj.card[0]]
                    
            for card_obj in cards:
                if card_obj.card[1] == game.trump_suit and trump_cards_vals[card_obj.card[0]] > max_val:
                    valid_cards.append(card_obj)
                    
            #If not, If you have any trumps
            if not valid_cards:
                for card_obj in cards:
                    if card_obj.card[1] == suit:
                        valid_cards.append(card_obj)
            #If not, any card
            return valid_cards if valid_cards else cards
        
        #Check if there is a trump
        trump_in_deck = False
        for card_obj in self.played_cards:
            if card_obj.card[1] == game.trump_suit:
                trump_in_deck = True
                break
        
        if trump_in_deck:
            #If you have cards of the same suit
            for card_obj in cards:
                if card_obj.card[1] == suit:
                    valid_cards.append(card_obj)
                     
            #If not, If you have bigger trump cards
            if not valid_cards:
                
                if len(self.played_cards) > 1:
                    if len(self.played_cards) - 2 == who_takes[0]:
                        return cards
                    
                max_val = 0
                for card_obj in self.played_cards:
                    if card_obj.card[1] == suit:
                        if max_val < trump_cards_vals[card_obj.card[0]]:
                            max_val = trump_cards_vals[card_obj.card[0]] 
                
                for card_obj in cards:
                    if card_obj.card[1] == game.trump_suit and trump_cards_vals[card_obj.card[0]] > max_val:
                        valid_cards.append(card_obj)
            
            #If not, every card    
            return valid_cards if valid_cards else cards
                
        
        #If you have cards of the same suit
        for card_obj in cards:
            if card_obj.card[1] == suit:
                valid_cards.append(card_obj)         
        
        #If not, if you have trump cards       
        if not valid_cards:
            if len(self.played_cards) > 1:
                if len(self.played_cards) - 2 == who_takes[0]:
                    return cards
                
            for card_obj in cards:
                if card_obj.card[1] == game.trump_suit:
                    valid_cards.append(card_obj)
                    
        #If not, any card         
        return valid_cards if valid_cards else cards
        
    def main_game_manager(self):
        valid_cards = self.get_valid_cards(self.first_played_card_suit, self.turn)
        for i, card in enumerate(valid_cards):
            if self.turn == 0:
                card.show_prompt()
            if Input.get_key_down(str(card.index + 1)):
                if self.first_played_card_suit == None:
                    self.first_played_card_suit = valid_cards[i].card[1]
                self.play_card(card, self.turn)
                self.game_state = GameState.WAITINGFORCARD.value
            
    def bot_manager(self):
        
        '''
        Test with a random bot TM. The state of the art Random AI which outperforms about 40% of all Bazar Blot players.
        '''
        
        #self.auction_curr_num[self.turn] = random.choice(["Pass", self.auction_start_num + 1, self.auction_start_num + 2])
        self.auction_curr_num[self.turn] = "Pass"
        self.chosen_suit[self.turn] = random.choice([0,1,2,3,4])
        self.auction_start_num = self.auction_curr_num[self.turn] + 1 if self.auction_curr_num[self.turn] != "Pass" else self.auction_start_num
        suit_to_symbol = ["♡", '♤', '♧', '♢', 'A']
        if self.auction_curr_num[self.turn] == "Pass":
            self.change_turn_auction(self.auction_curr_num[self.turn])
        else:
            if self.noTrumps:
                self.auction_result = [1, self.chosen_suit[self.turn], self.auction_curr_num[self.turn], self.turn % 2]
                self.change_turn_auction(f"{suit_to_symbol[self.chosen_suit[self.turn]]} {self.auction_curr_num[self.turn]} CP")
                
            else:
                self.auction_result = [0, self.chosen_suit[self.turn], self.auction_curr_num[self.turn], self.turn % 2]
                self.change_turn_auction(f"{suit_to_symbol[self.chosen_suit[self.turn]]} {self.auction_curr_num[self.turn]}")
        
    def change_turn_auction(self, text):
        if self.suits_prompt in self._GameManager__game_objects:
            self._GameManager__game_objects.remove(self.suits_prompt)
            
        if self.range_prompt in self._GameManager__game_objects:
            self._GameManager__game_objects.remove(self.range_prompt)
            
        if self.turn == 3:
            self.game_state = GameState.AUCTIONSUITS.value
        else:
            self.game_state = GameState.BOTTURNAUCTION.value
        
        if self.speech_bubbles[self.turn] not in self._GameManager__game_objects:
            self.add_object(self.speech_bubbles[self.turn])
            
        self.speech_bubbles[self.turn].set_text(text)
        self.speech_bubbles[self.turn].set_pos(self.turn)
        
        self.turn = (self.turn + 1) % 4
        
        for speech in self.speech_bubbles:
            if speech.text != "Pass":
                return
        
        if self.auction_result == [None, None, None, None]:
            self._GameManager__game_objects = []
            self.setup()
            return
        
        for speech in self.speech_bubbles:
            if speech in self._GameManager__game_objects:
                self._GameManager__game_objects.remove(speech)
        self.turn = (self.turn - 1) % 4
        #SET TRUMP SUIT
        self.speech = Speech_Bubble((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        
        text = ""
        suit_to_symbol = ["♡", '♤', '♧', '♢', 'A']
        if self.auction_result[0] == 1:
            text = f"{suit_to_symbol[self.auction_result[1]]} {self.auction_result[2]} CP"
        else:
            text = f"{suit_to_symbol[self.auction_result[1]]} {self.auction_result[2]}"
        self.speech.set_text(text)
        self.speech.set_pos(self.turn)
        self.add_object(self.speech)
        
        self.game.trump_suit = self.auction_result[1]
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
                self.change_turn_auction("Pass")
        
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
                self.change_turn_auction("Pass")
                
            if Input.get_key_down('d'):
                #TODO: Implement double down logic
                pass
            
            if Input.get_key_down('enter'):
                self.auction_start_num = self.auction_curr_num[self.turn] + 1
                suit_to_symbol = ['♡', '♤', '♧', '♢', 'A']
                if self.noTrumps:
                    self.auction_result = [1,self.chosen_suit[self.turn],self.auction_curr_num[self.turn],self.turn % 2]
                    self.change_turn_auction(f"{suit_to_symbol[self.chosen_suit[self.turn]]} {self.auction_curr_num[self.turn]} CP")
                else:
                    self.auction_result = [0,self.chosen_suit[self.turn],self.auction_curr_num[self.turn], self.turn % 2]
                    self.change_turn_auction(f"{suit_to_symbol[self.chosen_suit[self.turn]]} {self.auction_curr_num[self.turn]}")
                
                if self.noTrumps:
                    self.noTrumpsFinal = True

if __name__ == "__main__":
    game = Cards()
    manager = PlayersManager(game)
    manager.start()
    pass