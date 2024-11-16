from Belote_Logic import *
from playscii import GameObject
import numpy as np

class Left_Cards(GameObject): 
    index = 0
    def __init__(self, card, pos, main_player=False, left_right = False): 
        super().__init__(pos=pos, render=ascii_version_of_card(card) if main_player else ascii_version_of_hidden_card(left_right))
        self.index = Left_Cards.index
        self.card = card
        self.arr_index = Left_Cards.index
        Left_Cards.index += 1
        self.inplace = False
        self.to_play = False
        self.to_end_hand = False
        self.who_took = 0
        self.show_card()
        
    def __repr__(self) -> str:
        suits = ["♡", '♤', '♧', '♢']
        ranks = ["T", "K", "D", "V", "10", "9", "8", "7"]
        return f"{ranks[self.card[0]]} {suits[self.card[1]]}"
        
    
    def show_card(self):
        self.render = ascii_version_of_card(self.card)
        
    def hide_card(self):
        self.render = ascii_version_of_hidden_card(self.card)
       
    def update(self): 
        if not self.inplace:
            self.move_to_place()
        if self.to_play:
            self.play()
        if self.to_end_hand:
            self.end_hand()
    
    def move_to_place(self):
        animation_speed = 80
        card_length = 2
        left_offset = 2
        bottom_offset = (SCREEN_SIZE[1] - card_length * 6) // 2
        
        pos_to_move_x = left_offset
        pos_to_move_y = bottom_offset + self.index * card_length
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
        return
    
    def snap_in_place(self, x, y):
        self.x = x
        self.y = y
        self.inplace = True
        self.to_play = False
        self.to_fix_spacing = False
        self.to_end_hand = False
        return
    
    def play(self):
        animation_speed = 80
        pos_to_move_x = SCREEN_SIZE[0] // 2 - 22
        pos_to_move_y = SCREEN_SIZE[1] // 2 + 6
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
    
    def end_turn(self, to_who):
        self.to_end_hand = True
        self.who_took = to_who
        self.hide_card()
        self.end_hand()
    
    def end_hand(self):
        animation_speed = 80
        if self.who_took == 1:
            pos_to_move_x = 5
            pos_to_move_y = SCREEN_SIZE[1] - 5
        else:
            pos_to_move_x = SCREEN_SIZE[0] - 15
            pos_to_move_y = 5
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed

class Right_Cards(GameObject): 
    index = 0
    def __init__(self, card, pos, main_player=False, left_right = False): 
        super().__init__(pos=pos, render=ascii_version_of_card(card) if main_player else ascii_version_of_hidden_card(left_right))
        self.index = Right_Cards.index
        self.arr_index = Left_Cards.index
        Right_Cards.index += 1
        self.inplace = False
        self.to_play = False
        self.card = card
        self.to_end_hand = False
        self.who_took = 0
        self.show_card()
        
    def __repr__(self) -> str:
        suits = ["♡", '♤', '♧', '♢']
        ranks = ["T", "K", "D", "V", "10", "9", "8", "7"]
        return f"{ranks[self.card[0]]} {suits[self.card[1]]}"
        
    def show_card(self):
        self.render = ascii_version_of_card(self.card)
        
    def hide_card(self):
        self.render = ascii_version_of_hidden_card(self.card)
    
    def update(self): 
        if not self.inplace: 
            self.move_to_place()
        if self.to_play:
            self.play()
        if self.to_end_hand:
            self.end_hand()
    
    def move_to_place(self):
        animation_speed = 60
        card_length = 2
        left_offset = SCREEN_SIZE[0] - 14
        bottom_offset = (SCREEN_SIZE[1] - card_length * 6) // 2
        
        pos_to_move_x = left_offset
        pos_to_move_y = bottom_offset + self.index * card_length
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
        return
    
    def snap_in_place(self, x, y):
        self.x = x
        self.y = y
        self.inplace = True
        self.to_end_hand = False
        self.to_play = False
        return
    
    def play(self):
        animation_speed = 80
        pos_to_move_x = SCREEN_SIZE[0] // 2 + 14
        pos_to_move_y = SCREEN_SIZE[1] // 2 + 5
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
    
    def end_turn(self, to_who):
        self.to_end_hand = True
        self.who_took = to_who
        self.hide_card()
        self.end_hand()
    
    def end_hand(self):
        animation_speed = 80
        if self.who_took == 1:
            pos_to_move_x = 5
            pos_to_move_y = SCREEN_SIZE[1] - 5
        else:
            pos_to_move_x = SCREEN_SIZE[0] - 15
            pos_to_move_y = 5
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
    
    
class Top_Cards(GameObject): 
    index = 0
    def __init__(self, card, pos, main_player=False, left_right = False): 
        super().__init__(pos=pos, render=ascii_version_of_card(card) if main_player else ascii_version_of_hidden_card(left_right))
        self.index = Top_Cards.index
        self.arr_index = Left_Cards.index
        Top_Cards.index += 1
        self.inplace = False
        self.to_play = False
        self.card = card
        self.to_end_hand = False
        self.who_took = 0
        self.show_card()
        
    def __repr__(self) -> str:
        suits = ["♡", '♤', '♧', '♢']
        ranks = ["T", "K", "D", "V", "10", "9", "8", "7"]
        return f"{ranks[self.card[0]]} {suits[self.card[1]]}"

    def update(self): 
        if not self.inplace:
            self.move_to_place()
        if self.to_play:
            self.play()
        if self.to_end_hand:
            self.end_hand()
    
    def show_card(self):
        self.render = ascii_version_of_card(self.card)
    
    def hide_card(self):
        self.render = ascii_version_of_hidden_card(self.card)
    
    def move_to_place(self):
        animation_speed = 35
        card_length = 4
        left_offset = (SCREEN_SIZE[0] - card_length * 8) // 2
        bottom_offset = SCREEN_SIZE[1] - 2
        
        pos_to_move_x = left_offset + self.index * card_length
        pos_to_move_y = bottom_offset
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 0.5 and abs(diff_vector_y) < 0.5:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
    
    def snap_in_place(self, x, y):
        self.x = x
        self.y = y
        self.inplace = True
        self.to_play = False
        self.to_end_hand = False
        return
    
    def play(self):
        animation_speed = 80
        pos_to_move_x = SCREEN_SIZE[0] // 2 + 2
        pos_to_move_y = SCREEN_SIZE[1] // 2 + 6
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
    
    def end_turn(self, to_who):
        self.to_end_hand = True
        self.who_took = to_who
        self.hide_card()
        self.end_hand()
    
    def end_hand(self):
        animation_speed = 80
        if self.who_took == 1:
            pos_to_move_x = 5
            pos_to_move_y = SCREEN_SIZE[1] - 5
        else:
            pos_to_move_x = SCREEN_SIZE[0] - 15
            pos_to_move_y = 5
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed

class Main_Cards(GameObject): 
    index = 0
    def __init__(self, card, pos, main_player=False, left_right = False): 
        super().__init__(pos=pos, render=ascii_version_of_card(card) if main_player else ascii_version_of_hidden_card(left_right))
        self.index = Main_Cards.index
        self.arr_index = Left_Cards.index
        Main_Cards.index += 1
        self.inplace = False
        self.card = card
        self.to_play = False
        self.to_end_hand = False
        self.prompt_active = False
        self.who_took = 0
        
        self.NUM = """[{}]""".format('{num: <1}')
    
    def get_num_prompt(self, num: int) -> list:
        return self.NUM.format(num=str(num))
    
    def hide_card(self):
        self.render = ascii_version_of_hidden_card(self.card)
    
    def __repr__(self) -> str:
        suits = ["♡", '♤', '♧', '♢']
        ranks = ["T", "K", "D", "V", "10", "9", "8", "7"]
        return f"{ranks[self.card[0]]} {suits[self.card[1]]}"
    
    def update(self): 
        if not self.inplace:
            self.move_to_place()
        if self.to_play:
            self.play()
        if self.to_end_hand:
            self.end_hand()
    
    def remove_prompt(self):
        if self.prompt_active:
            self.render = self.render[:-7]
            self.prompt_active = False
    
    def show_prompt(self):
        if not self.prompt_active:
            self.render += "    " + self.get_num_prompt(self.index + 1)
            self.to_show_prompt = False
            self.prompt_active = True
    
    def move_to_place(self):
        animation_speed = 35
        card_length = 11
        bottom_offset = 10
        
        left_offset = (SCREEN_SIZE[0] - card_length * 8) // 2        
        pos_to_move_x = left_offset + self.index * card_length
        pos_to_move_y = bottom_offset
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 0.5 and abs(diff_vector_y) < 0.5:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
    
    def snap_in_place(self, x, y):
        self.x = x
        self.y = y
        self.inplace = True
        self.to_play = False
        self.to_end_hand = False
        return
    
    def play(self):
        Main_Cards.index -= 1
        animation_speed = 80
        pos_to_move_x = SCREEN_SIZE[0] // 2 - 10
        pos_to_move_y = SCREEN_SIZE[1] // 2 + 5
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
        
    def end_turn(self, to_who):
        self.to_end_hand = True
        self.who_took = to_who
        self.hide_card()
        self.end_hand()
        
    def end_hand(self):
        animation_speed = 80
        if self.who_took == 1:
            pos_to_move_x = 5
            pos_to_move_y = SCREEN_SIZE[1] - 5
        else:
            pos_to_move_x = SCREEN_SIZE[0] - 15
            pos_to_move_y = 5
        
        diff_vector_x = pos_to_move_x - self.x
        diff_vector_y = pos_to_move_y - self.y
        if abs(diff_vector_x) < 1 and abs(diff_vector_y) < 1:
            self.snap_in_place(pos_to_move_x, pos_to_move_y)
            return
        
        norm_factor = np.sqrt(diff_vector_x ** 2 + diff_vector_y ** 2)
        diff_vector_x = diff_vector_x / norm_factor
        diff_vector_y = diff_vector_y / norm_factor
        self.x += self.delta_time * diff_vector_x * animation_speed
        self.y += self.delta_time * diff_vector_y * animation_speed
        

       