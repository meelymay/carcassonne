colors = ['magenta','cyan','blue','yellow']

class Meeple:
    def __init__(self, player):
        self.player = player
        self.section = None
        self.color = player.get_color()

    def set_section(self, section):
        self.section = section

    def repossess(self, score):
        self.player.add_score(score)
        self.section = None

    def is_available(self):
        return self.section is None

    def displayable(self):
        if self.section is None:
            return self,self.player, self.section
        else:
            return self,self.player,self.section.displayable()
    
    def get_color(self):
        return self.player.get_color()
