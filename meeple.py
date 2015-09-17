COLORS = [
    '\033[96m',
    '\033[90m',
    '\033[94m',
    '\033[93m',
]

BOLD = '\033[1m'

NAME_COLORS = {}


class Meeple:

    def __init__(self, name):
        self.name = name
        if name not in NAME_COLORS:
            NAME_COLORS[name] = COLORS.pop() + BOLD
        self.color = NAME_COLORS[name]
        self.placed = False
        self.score = 0

    def place(self):
        self.placed = True

    def replace(self, score):
        self.score += score
        self.placed = False
