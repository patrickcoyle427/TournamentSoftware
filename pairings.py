#!/usr/bin/python3

"""
pairings.py - Creates pairings (list of who is playing against who in
              a tournament) and displays them. Writes the results back
              to the tournament's XML file.
"""

#TODO:
#
# Build a GUI
#
# implement the pairings, which has been finished in pairings_proto
#
# Have this read the tourament file to build pairings.
#
# Should be able to write click to enter pairings
# Also needs keyboard shortcuts for quick pairing entry
#
# Make best of 1 and best of 3 both work, but start with best of 1
#
# Window title should be the tournament's name in the file

import sys, random, os.path

import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QTableWidgetItem)
# More imports to come

class Pairings(QWidget):

    def __init__(self, tournament):

        super().__init__()

        if os.path.exists(tournament):

            self.tournament = tournament

            self.tree = self.load_tournament(self.tournament)

            self.tournament_root = self.tree.getroot()
            # self.tournament, self.tree, and self.tournament_root are all used
            # to help write the xml

            this_tournament_name = self.tournament_root[0][0].text
            # Used to make the GUI display the tournament name
            # as the title of the window

            self.initUI(this_tournament_name)

    def initUI(self, tournament_name):

        # Tournament Pairing window notes:
        # Left side will show the pairings, right side will be how
        # the user interacts with said pairings
        #
        # Left side: Table to display the pairings. Should be able to
        #            display the pairings in a variety of ways, including
        #            uncompleted matches, by table number or by player name
        #            user should be able to right click and enter a result.
        #
        # Right Side: Lets the user enter in results. Should give the user
        #             options to help filter pairings, by typing in the table
        #             number or by player's name.
        #             should be able to use the keyboard for entering in
        #             results quickly.

        ### Misc Window Settings ###

        self.setGeometry(200, 200, 700, 500)
        self.setWindowTitle(tournament_name)

        self.show()
        

    def load_tournament(self, tournament):

        # Helper function to load the event so it can be accessed by
        # the other methods

        tree = ET.parse(tournament)

        return tree
        # this is used by the __init__ to load the xml tree
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    pair = Pairings('Tournaments\\test ID6354692.xml')
    sys.exit(app.exec_())
