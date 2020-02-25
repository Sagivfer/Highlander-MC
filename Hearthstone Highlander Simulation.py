import numpy as np
import random
import matplotlib.pyplot as plt


def get_draws(duplicates, simulations):
    draws = np.zeros(30)
    for n_simulations in range(simulations):  # Looping over number of simulations
        if n_simulations == simulations - 1:
            return draws
        deck = create_deck(duplicates)  # Creating the deck
        dupes_drawn = np.zeros(duplicates)
        n_dupes_drawn = 0
        n_drawn_total = 0
        # While not all of the duplicates were drawn, continue drawing.
        while n_dupes_drawn < duplicates:
            # If it's a card that has a duplicate
            if deck[n_drawn_total] != 0:
                dupes_drawn[int(deck[n_drawn_total]) - 1] += 1
                if dupes_drawn[int(deck[n_drawn_total]) - 1] == 1:
                    n_dupes_drawn += 1
            n_drawn_total += 1
        draws[n_drawn_total] += 1 / simulations


# Function that picks the locations of the duplicates and places them there.
# We don't care about the non duplicates.
def create_deck(duplicates):
    deck = np.zeros(30)
    options = list(range(30))
    for dupe in range(duplicates):
        for i in range(2):
            loc = random.choice(options)
            options.remove(loc)
            deck[loc] = dupe + 1
    return deck


# Min number of duplicates and maximum to show on the graph.
def hist_n_charts(bottom, top, simulations):
    colors = ['blue', 'orange', 'red', 'pink', 'magenta', 'black', 'yellow', 'chocolate', 'gold']
    legends = []
    for n_dupes in range(bottom, top + 1):
        draws = get_draws(n_dupes, simulations)

        # Cumulative sum of the density function.
        cumm_sum = np.zeros(30)
        cumm_sum[0] = draws[0]
        for i in range(1, 29):
            cumm_sum[i] = cumm_sum[i - 1] + draws[i]

        legends.append(f'n_dupes = {n_dupes}')
        plt.bar(range(30), cumm_sum, color=colors[n_dupes])

    title = f'Cumulative probability function for drawing all dupes by draw \n n_simulations = {simulations}'
    plt.legend(legends)
    plt.title(title)
    plt.ylabel('Probability')
    plt.xlabel('Draw number')

    plt.show()


hist_n_charts(1, 8, 100000)
