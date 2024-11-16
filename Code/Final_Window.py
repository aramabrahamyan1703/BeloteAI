from playscii import GameObject
from Belote_Logic import SCREEN_SIZE

class ScoreWindow(GameObject):
    window = """\
      Us     │    Them                         
────────────────────────────
"""
    def __init__(self): 
        super().__init__(pos=(SCREEN_SIZE[0] // 2 - 15, SCREEN_SIZE[1] // 2 + 4), render="")
        self.render = ScoreWindow.window

    def set_final_score_text(self, new_score) -> list:
        edit = "{}|{}".format('{our: ^13}', '{their: ^13}')
        self.render = self.render + "\n" +edit.format(our=new_score[0],their=new_score[1])
        ScoreWindow.window = self.render
