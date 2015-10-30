import game
import random
import ai_player

BASE = ai_player.HEURISTICS

VALUES = [1000, 100, 10, 5, 3, 2, 1, .9, .7, .5, .2, .1, .01]
VALUES += map(lambda x: -x, VALUES) + [0]


def new_heuristics(heuristics):
    heuristics = dict(heuristics)
    for cat in heuristics:
        for k in heuristics[cat]:
            heuristics[cat][k] = random.choice(VALUES)
    return heuristics

if __name__ == '__main__':
    n = 25
    heur2 = BASE
    for i in range(n):
        heur1 = dict(BASE)
        heur2 = new_heuristics(heur2)
        strats = [heur1, heur2]
        g = game.Game(strats, robot=True)
        g.play()
