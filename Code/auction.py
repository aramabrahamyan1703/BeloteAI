from playscii import GameObject
from Belote_Logic import SCREEN_SIZE

SUITS = """\
┌─────────────────────────────────────────────────┐
│   Hearts[1]  Spades[2]  Clubs[3]  Diamonds[4]   │
│     Pass[p]                      No Trumps[n]   │
└─────────────────────────────────────────────────┘
"""

'''
Very bad way to handle spacing but it is what it is.
'''

RANGE = """\
┌─────────────────────────────────────────────────┐
│ Back[ESC]                           Call[ENTER] │
│{}│
│ Pass[p]           Capot[c]           Coinche[d] │        
└─────────────────────────────────────────────────┘
""".format('{num: ^49}')


SPEECH_BUBBLE = """\
┌────────────────┐
│{}│
└────────────────┘                     
""".format('{text: ^16}')


COINCHE_PROMPT = """\
┌────────────────┐
│   Coinche[d]   │
└────────────────┘                     
"""

class Suits_Prompt(GameObject):
    def __init__(self, pos): 
        super().__init__(pos=pos, render=SUITS)

class Range_Prompt(GameObject):
    def __init__(self, pos): 
        super().__init__(pos=pos, render=RANGE)
    
    def set_num(self, num):
        self.render = RANGE.format(num=f"<- {num} ->")

class Speech_Bubble(GameObject):
    def __init__(self, pos): 
        super().__init__(pos=pos, render=SPEECH_BUBBLE)
        self.text = 0
    
    def set_text(self, text):
        self.render = SPEECH_BUBBLE.format(text=text)
        self.text = text
        
    def set_pos(self, turn):
        pos_to_move_x = 0
        pos_to_move_y = 0
        
        '''
        Location to put the bubble depending on whose turn it is.
        Could be written without the if's using some function, but it's fast enough. 
        '''
        if turn == 0:
            card_length = 11
            bottom_offset = 10

            left_offset = (SCREEN_SIZE[0] - card_length * 8) // 2        
            pos_to_move_x = left_offset + 3.2 * card_length
            pos_to_move_y = bottom_offset + 4.5
            
            
        if turn == 1: 
            card_length = 2
            left_offset = 2
            bottom_offset = (SCREEN_SIZE[1] - card_length * 6) // 2

            pos_to_move_x = left_offset
            pos_to_move_y = bottom_offset * card_length + 5
   
        if turn == 2:
            card_length = 4
            left_offset = (SCREEN_SIZE[0] - card_length * 8) // 2
            bottom_offset = SCREEN_SIZE[1] - 2

            pos_to_move_x = left_offset + 9 * card_length
            pos_to_move_y = bottom_offset
        
        if turn == 3:
            card_length = 2
            left_offset = SCREEN_SIZE[0] - 14
            bottom_offset = (SCREEN_SIZE[1] - card_length * 6) // 2

            pos_to_move_x = left_offset - 6
            pos_to_move_y = bottom_offset * card_length + 5
            
        self.x = pos_to_move_x
        self.y = pos_to_move_y
    

