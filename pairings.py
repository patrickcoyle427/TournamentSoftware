#!/usr/bin/python3

'''
pairings.py - prototype pairings for the tournament software

'''
import random

from operator import itemgetter

# TO DO:
# Make tiebreakers?

def create_to_pair(players):

    # creates the structure that the pairings will use to calculate opponents

    to_pair = [[player, 0, 0, 0] for player in players]

        # The numbers corrispond to number of wins, number of draws,
        # and total points.

        # Draws are worth 1 point, wins are worth 3 points. Total points is the sum of
        # 3(wins) + draws

    testing = [['Test, Player', 3, 0, 0], ['1Test, Player', 3, 0, 0], ['2Test, Player', 3, 0, 0],
               ['3Test, Player', 6, 0, 0]]

    for player in testing:

               player[3] = player[1] + player[2]
               to_pair.append(player)

    # the above code is for testing purposes. It won't be in the finished code.

    to_pair = sorted(to_pair, key=itemgetter(1))
    # Sorts the list in ascending order based on the total points the players have.

    to_pair.reverse()
    # Reverses the to_pair list so that it is in descending order. Players with the most points
    # are always paired first

    return(to_pair)

def create_points_container(to_pair):

    points_container = {}

    for player in to_pair:

        total_points = player[3]

        if points_container.get(total_points) == None:

            points_container[total_points] = []

        points_container[total_points].append(player)

    return points_container

        # The lists that are generated here will be checked in the next section that actually creates
        # the pairings for the players.

def pair_players(to_pair):

    bye_granted = False

    pairings = []

    already_paired = []

    # Holds the names of players who have already been paired. They will be skipped
    # over in the for loop if they already do have one.

    for player in to_pair:

        if player not in already_paired:

            total_points = player[3]

            # Finds the total points the player hasn't been paired
            # if they HAVE already been paired, they are skipped over.

            if points_container[total_points]:

                # Checks if the list has more than 0 players. 

                match_exists = False

                points_to_check = total_points

                # if match_exists is False, there is no player to match up against the opponent
                # currently, and one needs to be found. If none around found in the player's
                # total_points is saved in a variable because if no matches are found, the player's
                # points are decremented by 1 to see if any opponents at a lower point value exist
                # to play against

                # If points_to_check ever reaches -1, the player is given a bye, which is a free win
                # because of an uneven number of players.

                while match_exists == False:

                # Check to see if there is anyone that can play against the player

                    if points_container.get(points_to_check) != None:

                        for opponent in points_container[points_to_check]:

                            # checks all the opponents in the player's point bracket to see if there is
                            # anyone who hasn't been paired. If there is someone this loop is broken and
                            # a pairing is found.

                            if opponent not in already_paired and opponent != player:

                                match_exists = True
                                break

                                # Breaks out of this loop if a match can be found.
                                

                    if match_exists == False:

                        points_to_check -= 1
                        # player's points decremented to see if there are any more players

                        if points_to_check == -1:

                            # If no match is found, the player's points to check will hit -1.
                            # if -1 is reached that there is an odd number of players in the event,
                            # in which case the player receives a free win.

                            pairings.append((player, ['BYE', 0, 0, 0]))
                            already_paired.append(player)
                            match_exists = True
                            bye_granted = True

                if bye_granted == False:

                    # The bye is always the last pairing created.
                    # If a bye is granted that means a pairing doesn't need to be found.

                    possible_opponent = random.choice(points_container[points_to_check])

                    while possible_opponent in already_paired or possible_opponent == player:

                        possible_opponent = random.choice(points_container[points_to_check])

                        # Keeps selecting random players until one that can be paired is found

                    pairing = (player, possible_opponent)

                    already_paired += list(pairing)

                    pairings.append(pairing)

    return pairings

def print_pairings(pairings):

    current_table_number = 0

    for pairing in pairings:

        current_table_number += 1

        print('{0}. {1} ({2} points) VS {3} ({4} points)'.format(current_table_number,
                                                        pairing[0][0], pairing[0][3],
                                                        pairing[1][0], pairing[1][3]))
                                        

if __name__ == '__main__':

    # Dict that will hold sorted players

    players = ['Nifterik, Emma', 'Mathieson, Harith',
           'Terry, Methoataske', 'Bell, Naseer',
           'Hamilton, Prasad', 'Kiefer, Yeong-Cheol',
           'Li, Mererid', 'Linville, Dieuwert',
           'Pat Coyle', 'Mitty Coyle']
    
    # Players list will be pulled from the XML file normally

    player_list_to_pair = create_to_pair(players)

    points_container = create_points_container(player_list_to_pair)

    pairings = pair_players(player_list_to_pair)

    print_pairings(pairings)
