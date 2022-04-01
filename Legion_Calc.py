import numpy as np
from datetime import datetime
import random


def dice_results(red_dice_in_pool=0, black_dice_in_pool=0, white_dice_in_pool=0):

    red_dice = [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]
    black_dice = [[1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]
    white_dice = [[1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]

    all_dice = [red_dice, black_dice, white_dice]

    x = 0
    dice_result = []
    dice_rolled = [red_dice_in_pool, black_dice_in_pool, white_dice_in_pool]

    for dice in dice_rolled:
        for number in range(0, dice):
            dice_result.append(random.choice(all_dice[x]))
        x += 1

    return dice_result


def dice_reroll(dice_result, red_dice_in_pool=0, black_dice_in_pool=0, white_dice_in_pool=0, precise=0,
                surge_tokens=0, critical=0, surge=0, cover=0, sharpshooter=0, total_impact=0, armor=0):

    red_dice = [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]
    black_dice = [[1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]
    white_dice = [[1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]

    dice_max_reroll = 2 + precise
    dice_to_reroll = np.zeros(red_dice_in_pool + black_dice_in_pool + white_dice_in_pool)

    reroll_used = 0
    die_checker = 0
    reroll_checker = 0
    crits_used = 0
    surges_used = 0
    hits_used = 0
    surge_tokens_used = 0

    hits = 0
    crits = 0
    surges = 0
    for side in dice_result:
        hits += side[0]
        crits += side[1]
        surges += side[2]

    crit_fishing = False

    for die in dice_result[::-1]:
        if die == [0, 0, 0]:
            # blank side reroll
            dice_to_reroll[die_checker] = 1
        elif die == [0, 0, 1]:
            if surge == 2:
                # don't reroll
                die_checker += 1
                continue
            elif critical > 0 and critical > crits_used and surges > surges_used:
                # don't reroll
                crits_used += 1
                surges_used += 1
            elif surge == 1:
                # don't reroll unless crit fishing
                if crit_fishing:
                    dice_to_reroll[die_checker] = 1
                else:
                    surges_used += 1
            elif surge_tokens > surge_tokens_used:
                # don't reroll unless crit fishing
                if crit_fishing:
                    dice_to_reroll[die_checker] = 1

                else:
                    surges_used += 1
                    surge_tokens_used += 1
            else:
                # reroll dead surge
                dice_to_reroll[die_checker] = 1
        elif die == [1, 0, 0]:
            # don't reroll unless crit fishing
            if crit_fishing:
                dice_to_reroll[die_checker] = 1
        elif die == [0, 1, 0]:
            # don't reroll crits you numpty
            die_checker += 1
            continue
        else:
            print('BAD DICE SIDE: SOMTHING WRONG')
            print(die)
        die_checker += 1

    dice_to_reroll = dice_to_reroll[::-1]
    for reroll_decision in dice_to_reroll:
        if reroll_decision == 1 and dice_max_reroll > reroll_used:
            # determine dice color and reroll
            if reroll_checker < red_dice_in_pool:
                rerolled_die = random.choice(red_dice)
                # dt = 'red'
            elif reroll_checker < red_dice_in_pool + black_dice_in_pool:
                rerolled_die = random.choice(black_dice)
                # dt = 'black'
            elif reroll_checker < red_dice_in_pool + black_dice_in_pool + white_dice_in_pool:
                rerolled_die = random.choice(white_dice)
                # dt = 'white'
            else:
                print("You've met with a terrible fate, haven't you?")
                print(reroll_checker)
                rerolled_die = [0, 0, 0]

            # replace die
            # print('replacing ' + dt + ' dice result ' + str(dice_result[reroll_checker]) +
            # ' with ' + str(rerolled_die))
            dice_result[reroll_checker] = rerolled_die
            reroll_used += 1

        reroll_checker += 1
    return dice_result


def dice_modifiers(dice_result, red_dice_in_pool=0, black_dice_in_pool=0, white_dice_in_pool=0, aim_tokens=0, precise=0,
                   surge_tokens=0, critical=0, surge=0, cover=0, sharpshooter=0, total_impact=0, armor=0):
    """
    aim/precise
    marksman
    surge/critical/surge token
    cover/sharpshooter
    impact/weakpoints
    armor

    Mod Array
    [aim tokens, precise, surge tokens #, critical x, surge(0 - none, 1- hits, 2- crits),
    cover(0-none, 1-light, 2-heavy), sharpshooter x, impact x + weakpoints, armor(0 none, #-amount, 99-all)]

    def mods
    [surge(0 - none, 1 - block), surge token #, dodge token, pierce, impervious, immune:pierce]
    """

    # aim logic here
    if aim_tokens > 0:
        for token in range(0, aim_tokens):
            aim_tokens -= 1
            dice_reroll(dice_result, red_dice_in_pool=red_dice_in_pool,
                        black_dice_in_pool=black_dice_in_pool,
                        white_dice_in_pool=white_dice_in_pool, precise=precise,
                        surge_tokens=surge_tokens, critical=critical, surge=surge, cover=cover,
                        sharpshooter=sharpshooter, total_impact=total_impact, armor=armor)

    # marksman logic here, no idea what does

    # Smash Dice Together
    hits = 0
    crits = 0
    surges = 0
    for side in dice_result:
        hits += side[0]
        crits += side[1]
        surges += side[2]

    dice_totals = [hits, crits, surges]

    # convert surges/use surge tokens/critical
    if surge_tokens + critical + surge > 0 and dice_totals[2] > 0:
        # Surge for Crits
        if surge == 2:
            dice_totals[1] += dice_totals[2]
            dice_totals[2] = 0

        # Critical x
        if critical > 0 and dice_totals[2] > 0:
            dice_totals[1] += min(dice_totals[2], critical)
            dice_totals[2] -= min(dice_totals[2], critical)

        # Surge for hits
        if surge == 1 and dice_totals[2] > 0:
            dice_totals[0] += dice_totals[2]
            dice_totals[2] = 0

        # Surge token
        if surge_tokens > 0 and dice_totals[2] > 0:
            dice_totals[0] += min(dice_totals[2], surge_tokens)
            dice_totals[2] -= min(dice_totals[2], surge_tokens)

    # remove hits for cover/reduce cover with sharpshooter
    if cover - sharpshooter > 0:
        cover_total = cover - sharpshooter
        dice_totals[0] = max(dice_totals[0] - cover_total, 0)

    # take armor into account
    if armor > 0:
        # convert impact and weak points into crits
        dice_totals[1] += min(dice_totals[0], total_impact)
        dice_totals[0] -= min(dice_totals[0], total_impact)

        # remove hits from armor
        dice_totals[0] -= min(dice_totals[0], armor)

    return dice_totals


def defense_dice(dice_totals, def_dice_type, surge=0, surge_token=0, dodge_token=0, pierce=0, impervious=0,
                 immune_pierce=0):
    # blocks
    # surges
    # pierce/impervious/immune:pierce
    red_dice = [[1, 0], [1, 0], [1, 0], [0, 1], [0, 0], [0, 0]]
    white_dice = [[1, 0], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0]]

    if def_dice_type == 'white':
        def_dice = white_dice
    elif def_dice_type == 'red':
        def_dice = red_dice
    else:
        print("Bad Defense Dice, try 'white' or 'red'!")
        return dice_totals

    # dodge token stuff here
    dice_totals[0] -= min(dice_totals[0], dodge_token)

    temp_surge_token_pool = surge_token
    def_pool = []

    for number in range(0, dice_totals[1] + dice_totals[0] + min(pierce, impervious)):
        def_pool.append(random.choice(def_dice))

    blocks = 0
    for outcome in def_pool:
        if surge == 1:
            blocks += outcome[0] + outcome[1]
        elif temp_surge_token_pool > 0 and outcome[1] > 0:
            blocks += outcome[0] + outcome[1]
            temp_surge_token_pool -= 1
        else:
            blocks += outcome[0]

    if pierce > 0 and immune_pierce == 0:
        blocks = max(blocks - pierce, 0)

    damage_totals = dice_totals[0] + dice_totals[1] - blocks

    return damage_totals


"""
Mod Array
[aim tokens, precise, surge tokens #, critical x, surge(0 - none, 1- hits, 2- crits), cover(0-none, 1-light, 2-heavy), 
sharpshooter x, impact x + weak points, armor(0 none, #-amount, 99-all)]

def mods
[surge(0 - none, 1 - block), surge token #, dodge token, pierce, impervious, immune:pierce]
"""

# Import from file row
# Export To file
# High Velocity
# Han's Reroll
# Outmanouver
# Crit Fishing

start = datetime.now()
red_dice_in_pool = 0
black_dice_in_pool = 6
white_dice_in_pool = 2
pdf = np.zeros(red_dice_in_pool + black_dice_in_pool + white_dice_in_pool+1)

for simulation in range(0, 100000):
    test_roll = dice_results(red_dice_in_pool=red_dice_in_pool, black_dice_in_pool=black_dice_in_pool,
                             white_dice_in_pool=white_dice_in_pool)
    test_atk_mods = dice_modifiers(test_roll, red_dice_in_pool=red_dice_in_pool, black_dice_in_pool=black_dice_in_pool,
                                   white_dice_in_pool=white_dice_in_pool, aim_tokens=2,
                                   precise=0, surge_tokens=0, critical=0, surge=0, cover=0, sharpshooter=0,
                                   total_impact=0,
                                   armor=0)
    test_def_roll = defense_dice(test_atk_mods, 'red', surge=0, surge_token=0, dodge_token=0, pierce=0, impervious=0,
                                 immune_pierce=0)
    pdf[test_def_roll] += 1

pdf_perc = pdf/sum(pdf)

output = []
output_header = [0, 0]
x = 0
ev = 0
for i in pdf_perc:
    output.append('{0:.4f}%'.format((i * 100)))
    ev += i * x
    x += 1

cdf = []
snowball = 0
for i in pdf_perc[::-1]:
    snowball += i
    cdf.append('{0:.4f}%'.format((snowball * 100)))

cdf = cdf[::-1]

output_header[1] = '{0:.2f}'.format(ev)
output_header[0] = 'name of roll' #make into params at some point
print(output_header)
print(output)
print(cdf)
print("done:" + str(datetime.now()-start))
