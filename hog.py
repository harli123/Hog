"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
from operator import itemgetter


GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    '''HLI Code starts here'''
    n = 0
    outcome = []
    score = 0
    while n < num_rolls:
        outcome.append(dice()) 
        n += 1
    #print (outcome) # checks what dice rolls i have captured
    if 1 in outcome:                      # pig out check  
        return 1
    else:
        for i in range(0, num_rolls):
            score = score + outcome[i]
        return score
    '''HLI Code ends here'''

#print(roll_dice(3,make_test_dice(4,5,1))) #Was a test for HLI for roll_dice function

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    ''' HLI Code starts here'''
    digits = [int(i) for i in str(opponent_score)]              # creating a list of digits of the opposing player's score
    if num_rolls == 0:                                          # the free bacon check
        return max(digits) + 1                                  # free bacon implementation
    else:                                                       # all other rolling scenarios
        return roll_dice(num_rolls, dice)
    '''HLI Code ends here'''

#print (take_turn(0,29,make_test_dice(4,3,2))) #was a test for HLI for take_turn function

# Playing a game

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    ''' HLI Code starts here'''
    if (score + opponent_score) % 7 == 0:    #hog wild check
        return four_sided
    else:
        return six_sided
    '''HLI Code ends here'''


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    score, opponent_score = 0, 0
    "*** YOUR CODE HERE ***"
    ''' HLI code starts Here'''
    while score < goal and opponent_score < goal:
        #the beginning of player 0's turn
        who = 0
        score = take_turn(strategy0(score, opponent_score), opponent_score, select_dice(score, opponent_score)) + score #player 0's score at end of his roll
        #if score > goal:                                                                                               #capping the score to goal, commented out as not part of game rules
        #    score = goal
        if score * 2 == opponent_score or score / 2 == opponent_score:                                                  #swine swap check after each player rolls and scores
            score, opponent_score = opponent_score, score
        # end of player 0's turn
        #print (score)
        if score >= goal or opponent_score >= goal:                                                                     #checking after each roll if someone has made it to goal yet if so end the loop / end game
            break
        
        #beginning of player 1's turn
        who = 1
        opponent_score = take_turn(strategy1(opponent_score, score), score, select_dice(score, opponent_score)) + opponent_score
        #if opponent_score > goal:                                                                                      #capping the score to goal, commented out as not part of game rules
        #    opponent_score = goal
        if score * 2 == opponent_score or score / 2 == opponent_score:                                                  #swine swap check after each player rolls and scores
            score, opponent_score = opponent_score, score
        #end of player 1's turn
        print (score,opponent_score)
    '''HLI code ends here'''
    return score, opponent_score  # You may wish to change this line.



#######################
# Phase 2: Strategies #
#######################

# Basic Strategy


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    
    """ HLI code starts here"""
    def avg_func(*args):
        counter = 0
        results = []
        while counter < num_samples:
            results.append(fn(*args))
            counter += 1
        return sum(results)/len(results)
    
    return avg_func

    "HLI Code ends here"

"""HLI testing make_averaged
dice = make_test_dice(3,1,5,6)
averaged_dice = make_averaged(dice,1000)
print(averaged_dice())
print(make_averaged(roll_dice,1000)(2,dice))
"""


def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """
    "*** YOUR CODE HERE ***"

    """HLI code starts here"""
    num_die = 1 
    avg_list = []
    while num_die < 11:
        temp_pair = (make_averaged(roll_dice,1000)(num_die,dice),num_die)                            #creating a temporary tuple to use for the print statement along with the population of the list to ensure that what is printed exactly matches what is in the list as each call to make_averaged will return a slightly different number even if num_samples is high)   
        avg_list.append(temp_pair)                                                                   #creating a list of tuples with each tuple have the first position be the average score and 2nd position the number of dice used
        #print (avg_list)                                                                            #this was used to check to make sure list matched print statements (didn't before)
        print(num_die," dice scores ",temp_pair[0], " on average")                  
        num_die += 1
    
    max_num_die_pair = max(avg_list, key = itemgetter(0))                                            #max function by default iterates along the list of tuples and returns the tuple with the highest combined pair value therefore need to use itemgetter to only compare the first value in tuple (average score value)
    print (max_num_die_pair[1])                                                                      
    return max_num_die_pair[1]                                                                       #Since max functions keeps the value of the first value computed as max do not need to search for lowest # of dice required to achieve highest avg. score (if scnenario where there is a tie, ex. a die with only a 1) as I start with 1 die and move up to mulitple dice


# HLI testing for myself to ensure max_scoring_num_rolls worked correctly
#dice = make_test_dice(3)
#max_scoring_num_rolls(dice)
#dice = make_test_dice(1)
#max_scoring_num_rolls(dice)
max_scoring_num_rolls(six_sided)

"""HLI code ends here"""

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1



def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    
    """HLI code starts here"""
    digits = [int(i) for i in str(opponent_score)]                                      #creates list of digits of opposing player's score
    if max(digits) + 1 >= margin:
        return 0
    else:
        return num_rolls

#HLI testing below
#print (bacon_strategy(3,99))

    """"HLI code starts here"""



def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"

    """HLI code starts here"""

    digits = [int(i) for i in str(opponent_score)]                                      #creates list of digits of opposing player's score
    

    if (max(digits) + 1 + score) / 2 == opponent_score:                                 #Need to make sure the beneficial swap and detrimental swap checks are before the margin threshold check
        return num_rolls
    elif (max(digits) + 1 + score) * 2 == opponent_score:
        return 0
    elif max(digits) + 1 >= margin:
        return 0
    else:
        return num_rolls

    """HLI code ends here"""

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results



def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"
      
    digits = [int(i) for i in str(opponent_score)]                                      #creates list of digits of opposing player's score
    
    if (GOAL_SCORE - score) <= (max(digits) + 1) and (max(digits) + 1 + score) / 2 != opponent_score:
        return 0
    elif (score + opponent_score) % 7 == 0:                                                #on avg with a four_sided die (1 - 4) the best num_rolls is ~3-4 for an average score of ~4-5 pts. So decision if we have a "hog wild" situation is to compare this 4-5 pts with a free bacon strat assuming it doesn't resul in a bad swap 
        return swap_strategy(score,opponent_score, margin = 4, num_rolls = 3)
    elif (max(digits) + 1 + score) * 2 == opponent_score:
        return 0
    elif (opponent_score - score) > 30:
        return 9
    elif (opponent_score - 20) > score:
        return 8
    elif (score - opponent_score) > 15:
        return swap_strategy(score, opponent_score, margin = 6.5, num_rolls = 5)
    else:
        return swap_strategy(score, opponent_score, margin = 8, num_rolls = 6)
    




    

##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()

#print (play(always_roll(4), always_roll(3))) # test code for HLI to see what play fucntion is doing with particular strategies
