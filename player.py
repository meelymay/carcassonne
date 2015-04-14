from meeple import *

class Player:
    
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.color = colors.pop()
        self.meeples = [Meeple(self) for m in range(7)]

    def get_meeple(self):
        for meeple in self.meeples:
            if meeple.is_available():
                return meeple
        return None

    def num_meeples(self):
        mps = 0
        for meeple in self.meeples:
            if meeple.is_available():
                mps += 1
        return mps

    def add_score(self, score):
        self.score += score

    def get_color(self):
        return self.color
