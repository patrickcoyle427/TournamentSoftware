#!/usr/bin/python3

'''
pairings.py - prototype pairings for the tournament software

'''
import random

# TO DO:
# Make pairings work
# Make tiebreakers?
# 


players = ['Nifterik, Emma', 'Mathieson, Harith',
           'Terry, Methoataske', 'Bell, Naseer',
           'Hamilton, Prasad', 'Kiefer, Yeong-Cheol',
           'Li, Mererid', 'Linville, Dieuwert']

# Players list will be pulled from the XML file normally

to_pair = []

for player in players:

    to_pair.append([player, 0, 0, 0])

    # creates the structure that the pairings will use to calculate opponents

    # The numbers corrispond to number of wins, number of draws,
    # and total points.

    # Draws are worth 1 point, wins are worth 3 points. Total points is the sum of
    # 3(wins) + draws

    
points_container = {}
# Dict that will hold sorted players

for player in to_pair:

    if points_container.get(player[3]) == None:

        points_container[player[3]] = []

    points_container[player[3]].append(player)

# Plan:

# Create copies of these dictionary lists and use them to create pairings.
# This will try to pair as many people with the same points as possible, starting with the
# person with the highest number of points. If no player with the same points is available
# to be paired, then it will find players with less points than them to play against.
# this will be done by decrementing their points by 1 and then rechecking if there is anyone
# to pair against. If this number reaches -1, then they will receive a bye. A bye occurs when
# there is an uneven number of players, and the player who gets it receives a win for the round.


