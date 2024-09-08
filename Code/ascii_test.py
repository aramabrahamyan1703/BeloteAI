from playscii import GameObject, GameManager
from playscii.input import Input
from Belote_Logic import *


SCREEN_SIZE = (150, 40)

class Card_obj(GameObject): 
    def __init__(self, card, pos, main_player=False, left_right = False): 
        super().__init__(pos=pos, render=ascii_version_of_card(card) if main_player else ascii_version_of_hidden_card(left_right))

    def update(self): # This method is called every frame. self.delta_time is the time it took between the frames.
        
        pass
       
class PlayersManager(GameManager): # Inherits GameManager
   def __init__(self, cards): 
        super().__init__(SCREEN_SIZE) 
        
        self.main_cards = [] 
        for index, card in enumerate(cards[:8]):
            card_length = 11
            bottom_offset = 8
            left_offset = (SCREEN_SIZE[0] - card_length * 8) // 2
            self.main_cards.append(Card_obj(card, (left_offset + index * card_length, bottom_offset), True))

        self.left_bot_cards = []
        for index, card in enumerate(cards[8:16]):
            card_length = 2
            left_offset = 2
            bottom_offset = (SCREEN_SIZE[1] - card_length * 6) // 2
            self.left_bot_cards.append(Card_obj(card, (left_offset, bottom_offset + index * card_length), False, True))
            
        self.right_bot_cards = []
        for index, card in enumerate(cards[16:24]):
            left_offset = SCREEN_SIZE[0] - 14
            card_length = 2
            bottom_offset = (SCREEN_SIZE[1] - card_length * 6) // 2
            self.right_bot_cards.append(Card_obj(card, (left_offset, bottom_offset + index * card_length), False, True))

        self.top_bot_cards = []
        for index, card in enumerate(cards[24:32]):
            card_length = 4
            bottom_offset = SCREEN_SIZE[1] - 2
            left_offset = (SCREEN_SIZE[0] - card_length * 8) // 2
            
            self.top_bot_cards.append(Card_obj(card, (left_offset + index * card_length, bottom_offset), False, False))

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


if __name__ == "__main__":
    game = Cards()
    game.create_deck()
    manager = PlayersManager(game.deck)
    manager.start()
    pass

