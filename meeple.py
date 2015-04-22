class Meeple:

    def __init__(self, color):
        self.color = color
        self.placed = False
        self.score = 0

    def place(self):
        self.placed = True

    def replace(self, score):
        self.score += score
        self.placed = False
