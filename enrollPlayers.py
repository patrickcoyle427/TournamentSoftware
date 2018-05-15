#!/usr/bin/python3

'''
enrollPlayers.py - enroll players into an event and write them to
                   the tournament file created with createNewTournament.py

'''

# TODO:

# Add way to add own ID numbers instead of just using temp IDs
#
# make sure to clear any players that may have been in the XML document
# before writing names to this. The prototype currently is just adding more players
# to the xml file, which is intended, but not what I want for this
#
# add checks to make sure xml file exists
#
# Make the cells of the table able to be right clicked with custom
#   menu. You should be able to change the player's name or remove them
#   from the list

import sys, os

import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QTableWidgetItem, QAbstractItemView,
                             QLabel, QLineEdit, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QHeaderView)

from PyQt5.QtCore import Qt

'''

sys - used for safely exiting the program

os - used for checking the status of the tournament file

PyQt5.QtWidgets - Various methods for constructing a GUI

PyQt5.QtCore - Contains commonly used information, in this case sorting
               in ascending order

'''


class EnrollPlayers(QWidget):

    currentIDNum = 0

    def __init__(self, event):

        self.Event = event

        self.Tree = self.loadEvent(self.Event)

        self.Tournament = self.Tree.getroot()

        # self.event, self.tree, and self.tournament are all used
        # to help write the xml

        thisEventName = self.Tournament[0][0].text

        # Used to make the GUI display the tournament name
        # as the title of the window

        super().__init__()

        # Runs the __init__ of QWidget, which EnrollPlayers inherits from

        self.initUI(thisEventName)

    def initUI(self, eventName):

        window_layout = QHBoxLayout()
        self.setLayout(window_layout)
        window_layout.setSpacing(5)
        # Sets a horizontal layout for the window itself

        ### Enrolling Players Section ###
        
        add_player_layout = QVBoxLayout()
        add_player_layout.addStretch(1)

        first_name_layout = QHBoxLayout()
        first_name_layout.setSpacing(1)

        self.firstNameLabel = QLabel('First Name: ', self)

        self.playerFirstName = QLineEdit()
        self.playerFirstName.returnPressed.connect(self.addPlayer)
        self.playerFirstName.setFocus(True)
        # Line that holds the player's first name

        first_name_layout.addWidget(self.firstNameLabel)
        first_name_layout.addWidget(self.playerFirstName)

        add_player_layout.addLayout(first_name_layout)
        
        last_name_layout = QHBoxLayout()
        last_name_layout.setSpacing(2)

        self.lastNameLabel = QLabel('Last Name: ', self)

        self.playerLastName = QLineEdit()
        self.playerLastName.returnPressed.connect(self.addPlayer)
        # Line that holds the player's last name

        last_name_layout.addWidget(self.lastNameLabel)
        last_name_layout.addWidget(self.playerLastName)
        
        add_player_layout.addLayout(last_name_layout)

        button_layout = QHBoxLayout()

        self.enroll_button = QPushButton('Enroll Player', self)
        self.enroll_button.clicked.connect(self.addPlayer)
        self.enroll_button.setAutoDefault(True)

        button_layout.addWidget(self.enroll_button)

        self.clear_button = QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.setAutoDefault(True)

        button_layout.addWidget(self.clear_button)

        add_player_layout.addLayout(button_layout)
        add_player_layout.addStretch(1)

        begin_event_layout = QHBoxLayout()

        begin_event_button = QPushButton('Begin Event', self)
        begin_event_button.clicked.connect(self.beginEvent)

        begin_event_layout.addStretch(1)

        begin_event_layout.addWidget(begin_event_button)

        add_player_layout.addLayout(begin_event_layout)

        ### Table View For Enrolled Players Section ###

        self.enrolled_table = QTableWidget()

        # The following options all change how the user interacts
        # with the table
        
        self.enrolled_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.enrolled_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.enrolled_table.verticalHeader().hide()
        # These prevent the user from editing the table cells,
        # Select the whole row when one is clicked
        # and hide the headers that appear to the left of the rows.
        
        self.enrolled_table.setColumnCount(2)
        self.enrolled_table.setHorizontalHeaderItem(0, QTableWidgetItem('Player'))
        self.enrolled_table.setHorizontalHeaderItem(1, QTableWidgetItem('ID'))
        self.enrolled_table.setColumnWidth(0, 235)
        self.enrolled_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode(2))
        # ResizeMode(2) is fixed size, meaning the user can't change the size
        # of the table

        window_layout.addWidget(self.enrolled_table)

        ### Misc Window Settings ###

        window_layout.addLayout(add_player_layout)

        self.setGeometry(200, 200, 700, 500)
        self.setWindowTitle(eventName)

        self.playerFirstName.setFocus(True)
        self.show()

    def addPlayer(self):

        firstName = self.playerFirstName.text()
        lastName = self.playerLastName.text()

        if firstName != '' or lastName != '':

            self.currentIDNum += 1

            tempID = 'TEMP{}'.format(str(self.currentIDNum).zfill(4))
            # Builds a temporary ID for the player.
            # Temp IDs are good for just getting a tournament up and running.

            self.enrolled_table.insertRow(self.enrolled_table.rowCount())

            currentRow = self.enrolled_table.rowCount() - 1

            self.enrolled_table.setItem(currentRow, 0, QTableWidgetItem('{}, {}'.
                                                        format(lastName, firstName)))
            self.enrolled_table.setItem(currentRow, 1, QTableWidgetItem(tempID))

            self.enrolled_table.setSortingEnabled(True)
            self.enrolled_table.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
            self.enrolled_table.setSortingEnabled(False)
            # This quickly enables sorting, sorts by the first column which is player
            # name, and then disables sorting so the user can't change the ordered.
            # This doesn't care about the order people were entered in, users just
            # need to be able to quickly see who is enrolled

            self.clear()
            # Calls clear to erase the entrant's name after they've been enrolled.

            self.playerFirstName.setFocus(True)
            # Returns the cursor to the first name box to make entering
            # players faster!

    def clear(self):

        # Helper function to clear the player's name after something is done,
        # such as when a player is entered

        self.playerFirstName.setText('')
        self.playerLastName.setText('')

        self.playerFirstName.setFocus(True)

    def getTableData(self):

        enrolled_players = []

        for row in range(self.enrolled_table.rowCount()):

            playerNameItem = self.enrolled_table.item(row, 0)
            playerIDItem = self.enrolled_table.item(row, 1)
            # gets the items from the table

            playerLastName, playerFirstName = playerNameItem.text().split(', ')
            # Split's first and last name, as they are combined in the cell
            # but saved separately in the xml document
            
            playerID = playerIDItem.text()

            enrolled_players.append((playerID, playerFirstName, playerLastName))
            # appends a tuple with the information to the enrolled_players list

        return enrolled_players
        # This is passed

    def loadEvent(self, event):

        # Helper function to load the event so it can be accessed by
        # the other methods

        tree = ET.parse(event)

        return tree
        # this is used by the __init__ to load the xml tree

    def beginEvent(self):

        enrolled_players = self.getTableData()

        players = self.Tournament[1]

        for idNum, first, last in enrolled_players:

            # Unpacks the tuples saved in enrolled_players
            # to be written to the xml file

            player = ET.SubElement(players, 'Player')

            idNumber = ET.SubElement(player, 'IDNumber')
            idNumber.text = idNum

            firstName = ET.SubElement(player, 'FirstName')
            firstName.text = first

            lastName = ET.SubElement(player, 'LastName')
            lastName.text = last

            wins = ET.SubElement(player, 'Wins')
            wins.text = '0'

            draws = ET.SubElement(player, 'Draws')
            draws.text = '0'

            # Wins and draws are both used during player pairings

        to_write = self.Tree

        to_write.write(self.Event,
                       encoding = 'utf-8',
                       xml_declaration = True)

        if __name__ == '__main__':

            self.close()
            # For testing, will be removed later
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    enroll = EnrollPlayers('Tournaments\\test ID6354692.xml')
    sys.exit(app.exec_())
