#!/usr/bin/python3

'''
enrollPlayers.py - enroll players into an event and write them to
                   the tournament file created with createNewTournament.py

'''

# TODO:

# Add way to add own ID numbers instead of just using temp IDs
#
# Create a GUI for editing a player's name
#
# Make variable names more consistent: stop using event and start using touranment

import sys, os.path

import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QTableWidgetItem, QAbstractItemView,
                             QLabel, QLineEdit, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QHeaderView,
                             QMessageBox, QMenu)

from PyQt5.QtCore import Qt

'''

sys - used for safely exiting the program

os.path - used for checking if the tournament file exists

PyQt5.QtWidgets - Various methods for constructing a GUI

PyQt5.QtCore - Contains commonly used information, in this case sorting
               in ascending order

'''


class EnrollPlayers(QWidget):

    currentIDNum = 0

    def __init__(self, event):

        super().__init__()
        # Runs the __init__ of QWidget, which EnrollPlayers inherits from

        if os.path.exists(event):
            # Check to make sure the event exists

            self.Event = event

            self.Tree = self.loadEvent(self.Event)

            self.Tournament = self.Tree.getroot()

            # self.event, self.tree, and self.tournament are all used
            # to help write the xml

            thisEventName = self.Tournament[0][0].text

            # Used to make the GUI display the tournament name
            # as the title of the window

            self.initUI(thisEventName)

        else:

            error = QMessageBox()

            error.setIcon(QMessageBox.Information)
            error.setText('No Tournament Found!')
            error.setWindowTitle('No Tournament Found')

            error.exec_()

            sys.exit(0) 

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

        begin_event_button = QPushButton('Begin Tournament', self)
        begin_event_button.clicked.connect(self.beginTournament)

        begin_event_layout.addStretch(1)

        begin_event_layout.addWidget(begin_event_button)

        add_player_layout.addLayout(begin_event_layout)

        ### Table View For Enrolled Players Section ###

        self.enrolled_table = QTableWidget()

        # The following options all change how the user interacts
        # with the table
        
        self.enrolled_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # These prevent the user from editing the table cells,
        self.enrolled_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Select the whole row when one is clicked
        self.enrolled_table.setSelectionMode(QAbstractItemView.SingleSelection)
        # Prevents selection of multiple rows.
        self.enrolled_table.verticalHeader().hide()
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

        if firstName.strip() != '' and lastName.strip() != '':

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
            # name, and then disables sorting so the user can't change the order.
            # This doesn't care about the order people were entered in, users just
            # need to be able to quickly see who is enrolled

            self.clear()
            # Calls clear to erase the entrant's name after they've been enrolled.

            self.playerFirstName.setFocus()
            # Returns the cursor to the first name box to make entering
            # players faster!

        else:

            nameError = QMessageBox()
            nameError.setIcon(QMessageBox.Information)
            nameError.setWindowTitle('Blank Name')

            if firstName.strip() == '':

                self.playerFirstName.setFocus()
                nameError.setText("The Player's first name is blank.")

            else:

                self.playerLastName.setFocus()
                nameError.setText("The Player's last name is blank.")

            nameError.exec_()

    def contextMenuEvent(self, event):

        selection = self.enrolled_table.selectedItems()

        if len(selection) > 0:

            table_menu = QMenu(self)

            renamePlayer = table_menu.addAction('Rename Player')
            dropPlayer = table_menu.addAction('Drop Player')

            action = table_menu.exec_(self.mapToGlobal(event.pos()))

            if action == dropPlayer:

                row = selection[0].row()

                self.enrolled_table.removeRow(row)

            self.enrolled_table.clearSelection()
            # Automatically clears the selection after it is right clicked
            # So the user doesn't accidently keep clicking the same cell

            elif action == renamePlayer:

                pass
                #TODO: Create a menu that pops up to edit the player's name.

            


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
        # This is passed to writeToFile

    def loadEvent(self, event):

        # Helper function to load the event so it can be accessed by
        # the other methods

        tree = ET.parse(event)

        return tree
        # this is used by the __init__ to load the xml tree

    def writeToFile(self, enrolled_players):

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

    def beginTournament(self):

        enrolled_players = self.getTableData()

        total_players = len(enrolled_players)

        if len(enrolled_players) < 4:

            # Prevents the user from creating an event with less than 4 players

            lessThan4Error = QMessageBox()
            lessThan4Error.setIcon(QMessageBox.Information)
            lessThan4Error.setText('A tournament cannot have less than 4 players!')
            lessThan4Error.setWindowTitle('Not Enough Players')

            # Tournaments with less than 4 players just don't work. With 4 players
            # You can have 3 rounds and a definite winner.

            self.playerFirstName.setFocus()

            lessThan4Error.exec_()

        else:

            eventCreated = QMessageBox()
            eventCreated.setIcon(QMessageBox.Information)
            eventCreated.setText('{} Players were enrolled.'.format(total_players))
            eventCreated.setWindowTitle('Players Successfully Enrolled')

            # Alerts the user that players have been entered, and gives the total number
            # so the user can double check how many people have been entered.

            eventCreated.exec_()

            self.writeToFile(enrolled_players)

            if __name__ == '__main__':

                self.close()
                # For testing, will be removed later
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    enroll = EnrollPlayers('Tournaments\\test ID6354692.xml')
    sys.exit(app.exec_())
