from Belote_Logic import *
from playscii import GameObject
import numpy as np

class Left_Cards(GameObject): 
    index = 0
    def __init__(self, card, pos, main_player=False, left_right = False): 
        super().__init__(pos=pos, render=ascii_version_of_card(card) if main_player else ascii_version_of_hidden_card(left_right))
        self.index = Left_Cards.index
        Left_Cards.index += 1
        self.inplace = False
        
    def update(self): # This method is called every frame. self.delta_time is the time it took between the frames.
        if not self.inplace:
            self.move_to_place()
        pass
    
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
        return

class Right_Cards(GameObject): 
    index = 0
    def __init__(self, card, pos, main_player=False, left_right = False): 
        super().__init__(pos=pos, render=ascii_version_of_card(card) if main_player else ascii_version_of_hidden_card(left_right))
        self.index = Right_Cards.index
        Right_Cards.index += 1
        self.inplace = False
    def update(self): # This method is called every frame. self.delta_time is the time it took between the frames.
        if not self.inplace: 
            self.move_to_place()
        pass
    
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
        return
    
class Top_Cards(GameObject): 
    index = 0
    def __init__(self, card, pos, main_player=False, left_right = False): 
        super().__init__(pos=pos, render=ascii_version_of_card(card) if main_player else ascii_version_of_hidden_card(left_right))
        self.index = Top_Cards.index
        Top_Cards.index += 1
        self.inplace = False
    def update(self): # This method is called every frame. self.delta_time is the time it took between the frames.
        if not self.inplace:
            self.move_to_place()
        pass
    
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
        return

class Main_Cards(GameObject): 
    index = 0
    def __init__(self, card, pos, main_player=False, left_right = False): 
        super().__init__(pos=pos, render=ascii_version_of_card(card) if main_player else ascii_version_of_hidden_card(left_right))
        self.index = Main_Cards.index
        Main_Cards.index += 1
        self.inplace = False
        
    def update(self): # This method is called every frame. self.delta_time is the time it took between the frames.
        if not self.inplace:
            self.move_to_place()
        pass
    
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
        return
       