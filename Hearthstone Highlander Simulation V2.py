'''
Written by Sagiv Ferster, B.SC in Industrial engineering
26/2/20
'''

import numpy as np
import random
import matplotlib.pyplot as plt


def get_draws(duplicates, n_special, simulations):
    draws = np.zeros(30)
    times_reno_before_dupes = np.zeros(2)
    reno_before_turn = np.zeros(30)
    reno_activated_by_turn = np.zeros(30)
    for n_simulations in range(simulations):  # Looping over number of simulations
        if n_simulations == simulations - 1:
            return draws, times_reno_before_dupes, reno_before_turn, reno_activated_by_turn
        deck = create_deck(duplicates)  # Creating the deck
        dupes_drawn = np.zeros(duplicates)
        n_dupes_drawn = 0
        n_leg_drawn = 0
        n_drawn_total = 0
        # While not all of the duplicates were drawn, continue drawing.
        reno_drawn = False
        flag = True
        added = False
        while flag:
            # If it's a card that has a duplicate
            if deck[n_drawn_total] > 0:
                dupes_drawn[int(deck[n_drawn_total]) - 1] += 1
                if dupes_drawn[int(deck[n_drawn_total]) - 1] == 1:
                    n_dupes_drawn += 1
                    if n_dupes_drawn == duplicates:
                        draws[n_drawn_total] += 1 / simulations

            # If we drew Reno then marking it as a "Success"
            elif deck[n_drawn_total] < 0:
                if deck[n_drawn_total] == -1:
                    reno_drawn = True
                n_leg_drawn += 1
            n_drawn_total += 1

            # Taking care of the case where there are none duplicates.
            if duplicates == 0:
                if reno_drawn:
                    flag = False

            # Loop condition
            elif n_dupes_drawn == duplicates:
                if reno_drawn:
                    flag = False

            # Mark the moment we draw reno and he is deactivated.
            elif reno_drawn and not added:
                added = True
                times_reno_before_dupes[1] += 1 / simulations

        # Calculation the probability of us having reno and him being activated by turn X
        reno_activated_by_turn[n_drawn_total - 1] += 1 / simulations


# Function that picks the locations of the duplicates and places them there.
# We don't care about the non duplicates.
def create_deck(duplicates, n_special=1):
    deck = np.zeros(30)
    options = list(range(30))
    for dupe in range(duplicates):
        for i in range(2):
            loc = random.choice(options)
            options.remove(loc)
            deck[loc] = dupe + 1
    for special in range(n_special):
        loc = random.choice(options)
        options.remove(loc)
        deck[loc] = -(special + 1)
    return deck


# Min number of duplicates and maximum to show on the graph.
def hist_n_charts(bottom, top, bottom_leg, top_leg, simulations):
    colors = ['blue', 'orange', 'red', 'pink', 'magenta', 'black', 'yellow', 'chocolate', 'gold']
    legends = []
    fig_draws = plt.figure()
    fig_draws.suptitle(f'Cumulative probability function for drawing all dupes by draw \n n_simulations = {simulations}')
    ax_stacked = fig_draws.add_subplot((top - bottom) / 2, (top - bottom) / 2, top - bottom + 2)

    fig_after_drawn = plt.figure()
    fig_after_drawn.suptitle("Probability of drawing reno \n before all dupes were drawn")

    fig_before_turn = plt.figure()
    fig_before_turn.suptitle("Probability of drawing reno \n and him being activated before turn X")
    ax3_stacked = fig_before_turn.add_subplot((top - bottom) / 2, (top - bottom) / 2, top - bottom + 2)

    fig_activated_turn = plt.figure()
    fig_activated_turn.suptitle("Probability of having Reno \n and him being activated by turn X")
    ax4_stacked = fig_activated_turn.add_subplot((top - bottom) / 2, (top - bottom) / 2, top - bottom + 2)

    count = 1
    for n_dupes in range(bottom, top + 1):
        for n_special in range(bottom_leg, top_leg):
            draws, times_reno_before_dupes, reno_before_turn, activated_t = get_draws(n_dupes, n_special, simulations)
            times_reno_before_dupes[0] = 1 - times_reno_before_dupes[1]  # Summing to 1

            # Cumulative sum of the density function.
            cumm_sum = np.zeros(30)
            cumm_sum[0] = draws[0]

            cumm_sum_r = np.zeros(30)
            cumm_sum_r[0] = reno_before_turn[0]

            cumm_sum_a = np.zeros(30)
            cumm_sum_a[0] = activated_t[0]
            for i in range(1, 29):
                cumm_sum_a[i] = cumm_sum_a[i - 1] + activated_t[i]
                cumm_sum_r[i] = cumm_sum_r[i - 1] + reno_before_turn[i]
                cumm_sum[i] = cumm_sum[i - 1] + draws[i]

            ax2 = fig_after_drawn.add_subplot(n_special * (top - bottom) - 1, 2, count)
            ax2.set_title(f'n_dupes = {n_dupes}')
            ax2.set_ylabel('Probability')
            ax2.bar(['After', 'Before'], times_reno_before_dupes)

            count += 1

        ax3 = fig_before_turn.add_subplot((top - bottom) / 2, (top - bottom) / 2, count - 1)
        ax3.set_title(f'n_dupes = {n_dupes}')
        ax3.set_ylabel('Probability')
        ax3.set_xlabel('Draw number')
        ax3.bar(range(1, 31), cumm_sum_r)
        ax3_stacked.bar(range(1, 31), cumm_sum_r, color=colors[n_dupes])

        ax4 = fig_activated_turn.add_subplot((top - bottom) / 2, (top - bottom) / 2, count - 1)
        ax4.set_title(f'n_dupes = {n_dupes}')
        ax4.set_ylabel('Probability')
        ax4.set_xlabel('Draw number')
        ax4.bar(range(1, 31), cumm_sum_a)
        ax4_stacked.bar(range(1, 31), cumm_sum_a, color=colors[n_dupes])

        legends.append(f'n_dupes = {n_dupes}')

        ax = fig_draws.add_subplot((top - bottom) / 2, (top - bottom) / 2, n_dupes + 1)
        ax.set_title(f"n_dupes = {n_dupes}")
        ax.set_ylabel('Probability')
        ax.set_xlabel('Draw number')
        ax.bar(range(1, 31), cumm_sum, color=colors[n_dupes])
        ax_stacked.bar(range(1, 31), cumm_sum, color=colors[n_dupes])

    ax3_stacked.legend(legends)
    ax3_stacked.set_xlabel('Draw number')
    ax3_stacked.set_ylabel('Probability')

    ax4_stacked.legend(legends)
    ax4_stacked.set_xlabel('Draw number')
    ax4_stacked.set_ylabel('Probability')

    ax_stacked.legend(legends)
    ax_stacked.set_xlabel('Draw number')
    ax_stacked.set_ylabel('Probability')

    fig_draws.subplots_adjust(hspace=0.4, wspace=0.3)
    fig_draws.set_size_inches(10, 7)

    fig_before_turn.subplots_adjust(hspace=0.4, wspace=0.3)
    fig_before_turn.set_size_inches(10, 7)

    fig_after_drawn.subplots_adjust(hspace=0.4, wspace=0.3)
    fig_after_drawn.set_size_inches(10, 7)

    fig_activated_turn.subplots_adjust(hspace=0.5, wspace=0.3)
    fig_activated_turn.set_size_inches(10, 7)
    plt.show()


hist_n_charts(0, 6, 1, 2, 100000)
