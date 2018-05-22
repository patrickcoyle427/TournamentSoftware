#!/usr/bin/python3

"""
enrollPlayers.py - enroll players into an event and write them to
                   the tournament file created with createNewTournament.py

"""

# TODO:

# Add way to add own ID numbers instead of just using temp IDs

import sys, os.path

import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QTableWidgetItem, QAbstractItemView,
                             QLabel, QLineEdit, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QHeaderView,
                             QMessageBox, QMenu, QDialog)

from PyQt5.QtCore import Qt

"""

sys - used for safely exiting the program

os.path - used for checking if the tournament file exists

xml.etree.ElementTree - reads and writes to the tournament's xml doc, which contains
                        all the info th e tournament software needs to make
                        the tournament work.

PyQt5.QtWidgets - Various methods for constructing a GUI

PyQt5.QtCore - Contains commonly used information, in this case sorting
               in ascending order

"""


class EnrollPlayers(QWidget):

    current_id_num = 0

    def __init__(self, tournament):

        super().__init__()
        # Runs the __init__ of QWidget, which EnrollPlayers inherits from

        if os.path.exists(tournament):
            # Check to make sure the tournament exists

            self.tournament = tournament

            self.tree = self.loadTournament(self.tournament)

            self.tournament_root = self.tree.getroot()

            # self.tournament, self.tree, and self.tournament_root are all used
            # to help write the xml

            this_tournament_name = self.tournament_root[0][0].text

            # Used to make the GUI display the tournament name
            # as the title of the window

            self.initUI(this_tournament_name)

        else:

            error = QMessageBox()

            error.setIcon(QMessageBox.Information)
            error.setText('No Tournament Found!')
            error.setWindowTitle('No Tournament Found')

            error.exec_()

            sys.exit(0) 

    def initUI(self, tournamentName):

        window_layout = QHBoxLayout()
        self.setLayout(window_layout)
        window_layout.setSpacing(5)
        # Sets a horizontal layout for the window itself

        ### Enrolling Players Section ###
        
        add_player_layout = QVBoxLayout()
        add_player_layout.addStretch(1)

        first_name_layout = QHBoxLayout()
        first_name_layout.setSpacing(1)

        self.first_name_label = QLabel('First Name: ', self)

        self.player_first_name = QLineEdit()
        self.player_first_name.returnPressed.connect(self.addPlayer)
        self.player_first_name.setFocus(True)
        # Line that holds the player's first name

        first_name_layout.addWidget(self.first_name_label)
        first_name_layout.addWidget(self.player_first_name)

        add_player_layout.addLayout(first_name_layout)
        
        last_name_layout = QHBoxLayout()
        last_name_layout.setSpacing(2)

        self.lastNameLabel = QLabel('Last Name: ', self)

        self.player_last_name = QLineEdit()
        self.player_last_name.returnPressed.connect(self.addPlayer)
        # Line that holds the player's last name

        last_name_layout.addWidget(self.lastNameLabel)
        last_name_layout.addWidget(self.player_last_name)
        
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

        begin_tournament_layout = QHBoxLayout()

        begin_tournament_button = QPushButton('Begin Tournament', self)
        begin_tournament_button.clicked.connect(self.beginTournament)

        begin_tournament_layout.addStretch(1)

        begin_tournament_layout.addWidget(begin_tournament_button)

        add_player_layout.addLayout(begin_tournament_layout)

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
        self.setWindowTitle(tournamentName)

        self.player_first_name.setFocus(True)
        self.show()

    def addPlayer(self):

        first_name = self.player_first_name.text()
        lastName = self.player_last_name.text()

        if first_name.strip() != '' and lastName.strip() != '':

            self.current_id_num += 1

            tempID = 'TEMP{}'.format(str(self.current_id_num).zfill(4))
            # Builds a temporary ID for the player.
            # Temp IDs are good for just getting a tournament up and running.

            self.enrolled_table.insertRow(self.enrolled_table.rowCount())

            currentRow = self.enrolled_table.rowCount() - 1

            self.enrolled_table.setItem(currentRow, 0, QTableWidgetItem('{}, {}'.
                                                        format(lastName, first_name)))
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

            self.player_first_name.setFocus()
            # Returns the cursor to the first name box to make entering
            # players faster!

        else:

            nameError = QMessageBox()
            nameError.setIcon(QMessageBox.Information)
            nameError.setWindowTitle('Blank Name')

            if first_name.strip() == '':

                self.player_first_name.setFocus()
                nameError.setText("The Player's first name is blank.")

            else:

                self.player_last_name.setFocus()
                nameError.setText("The Player's last name is blank.")

            nameError.exec_()

    def contextMenuEvent(self, event):

        selection = self.enrolled_table.selectedItems()

        if len(selection) > 0:

            table_menu = QMenu(self)

            dropPlayer = table_menu.addAction('Drop Player')
            renamePlayer = table_menu.addAction('Rename Player')

            action = table_menu.exec_(self.mapToGlobal(event.pos()))

            if action == dropPlayer:

                row = selection[0].row()

                self.enrolled_table.removeRow(row)

            elif action == renamePlayer:

                player_last_name, player_first_name = selection[0].text().split(', ')

                editNameWindow = QDialog()
                # Creates a dialog box that will pop up if the user choses rename player

                dialogLayout = QVBoxLayout()

                ### Dialog First Name Change ###

                dialogFirstNameLayout = QHBoxLayout()
                editFirstNameLabel = QLabel('New First Name:')
                editFirstName = QLineEdit()
                editFirstName.setText(player_first_name)

                dialogFirstNameLayout.addWidget(editFirstNameLabel)
                dialogFirstNameLayout.addWidget(editFirstName)

                dialogLayout.addLayout(dialogFirstNameLayout)

                ### Dialog Last Name Change ###
                
                dialogLastNameLayout = QHBoxLayout()
                
                editLastNameLabel = QLabel('New Last Name:')
                editLastName = QLineEdit()
                editLastName.setText(player_last_name)

                dialogLastNameLayout.addWidget(editLastNameLabel)
                dialogLastNameLayout.addWidget(editLastName)

                dialogLayout.addLayout(dialogLastNameLayout)

                ### Dialog Buttons ###
                 
                dialogButtons = QHBoxLayout()
                
                editName = QPushButton('Edit Name')
                editName.clicked.connect(editNameWindow.accept)
                
                cancelName = QPushButton('Cancel')
                cancelName.clicked.connect(editNameWindow.reject)

                dialogButtons.addWidget(editName)
                dialogButtons.addWidget(cancelName)

                dialogLayout.addLayout(dialogButtons)

                ### Misc Window Settings ###
            
                editNameWindow.setWindowTitle('Change Player Name')
                editNameWindow.setGeometry(300, 300, 300, 100)
                editNameWindow.setLayout(dialogLayout)

                choice = editNameWindow.exec_()
                # Returns a number corresponding to the user's choice.
                # 1 = Accept (Hit the ok button)
                # 0 = Reject (Hit the cancel button)

                if choice == 1:

                    selection[0].setText('{}, {}'.format(editLastName.text(), editFirstName.text()))
                    
                    self.enrolled_table.setSortingEnabled(True)
                    self.enrolled_table.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
                    self.enrolled_table.setSortingEnabled(False)
                    # Resorts the players names after a name is changed
            
            self.enrolled_table.clearSelection()
            # Automatically clears the selection after it is right clicked
            # So the user doesn't accidently keep clicking the same cell


    def clear(self):

        # Helper function to clear the player's name after something is done,
        # such as when a player is entered

        self.player_first_name.setText('')
        self.player_last_name.setText('')

        self.player_first_name.setFocus(True)

    def getTableData(self):

        enrolled_players = []

        for row in range(self.enrolled_table.rowCount()):

            playerNameItem = self.enrolled_table.item(row, 0)
            playerIDItem = self.enrolled_table.item(row, 1)
            # gets the items from the table

            player_last_name, player_first_name = playerNameItem.text().split(', ')
            # Split's first and last name, as they are combined in the cell
            # but saved separately in the xml document
            
            playerID = playerIDItem.text()

            enrolled_players.append((playerID, player_first_name, player_last_name))
            # appends a tuple with the information to the enrolled_players list

        return enrolled_players
        # This is passed to writeToFile

    def loadTournament(self, tournament):

        # Helper function to load the event so it can be accessed by
        # the other methods

        tree = ET.parse(tournament)

        return tree
        # this is used by the __init__ to load the xml tree

    def writeToFile(self, enrolled_players):

        players = self.tournament[1]

        for idNum, first, last in enrolled_players:

            # Unpacks the tuples saved in enrolled_players
            # to be written to the xml file

            player = ET.SubElement(players, 'Player')

            idNumber = ET.SubElement(player, 'IDNumber')
            idNumber.text = idNum

            first_name = ET.SubElement(player, 'FirstName')
            first_name.text = first

            lastName = ET.SubElement(player, 'LastName')
            lastName.text = last

            wins = ET.SubElement(player, 'Wins')
            wins.text = '0'

            draws = ET.SubElement(player, 'Draws')
            draws.text = '0'

            # Wins and draws are both used during player pairings

        to_write = self.tree

        to_write.write(self.tournament,
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

            self.player_first_name.setFocus()

            lessThan4Error.exec_()

        else:

            tournament_created = QMessageBox()
            tournament_created.setIcon(QMessageBox.Information)
            tournament_created.setText('{} Players were enrolled.'.format(total_players))
            tournament_created.setWindowTitle('Players Successfully Enrolled')

            # Alerts the user that players have been entered, and gives the total number
            # so the user can double check how many people have been entered.

            tournament_created.exec_()

            self.writeToFile(enrolled_players)

            if __name__ == '__main__':

                self.close()
                # For testing, will be removed later
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    enroll = EnrollPlayers('Tournaments\\test ID6354692.xml')
    sys.exit(app.exec_())
