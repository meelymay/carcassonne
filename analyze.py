import matplotlib.pyplot as plt
import numpy as np
import train
import sys
import json


def create_and_save_plot(vals, scores, name):
    plt.plot(vals, scores, 'ro')
    plt.savefig(name)
    plt.clf()
    print 'created ', name


def color_map(val1, val2, scores, name):
    train.VALUES


def display_heuristic(strategy):
    for cat in strategy:
        print '\t', cat
        for opt in strategy[cat]:
            print '\t\t%s\t%s' % (opt, strategy[cat][opt])


def analyze(f, plots_dir):
    strats = []
    for l in f:
        game = json.loads(l)
        for p in ['IBM']:
            strats.append(game[p])
            display_heuristic(game[p]['strat'])
            print game[p]['score']
    print len(strats)

    ex = strats[0]['strat']
    all_vals = []
    for cat in ex:
        for opt in ex[cat]:
            vals = []
            scores = []
            for strat in strats:
                val = strat['strat'][cat][opt]
                score = strat['score']
                if val < 10 and val > -10:
                    vals.append(val)
                    scores.append(score)
            name = '%s/%s_%s' % (plots_dir, cat, opt)
            create_and_save_plot(vals, scores, name)


if __name__ == '__main__':
    t = sys.argv[1]
    plots_dir = sys.argv[2]
    f = open(t, 'r')
    analyze(f, plots_dir)
    f.close()
