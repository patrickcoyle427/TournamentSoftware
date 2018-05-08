#!/usr/bin/python3

'''
enrollPlayers.py - enroll players into an event and write them to
                   the tournament file created with createNewTournament.py

'''

# TODO:

# Implelment how the window will look. I think the enrollment section should
#     be on the left and the tableview of all the players should be right
#
# Have this load the XML tournament file and write the players to it
#
# Window title should display the tournament's name
#
# Add way to add own ID numbers instead of just using temp IDs
#
# Make addPlayer functional

import sys, os, random

import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QTableWidgetItem, QAbstractItemView,
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout)

from PyQt5.QtCore import Qt


class EnrollPlayers(QWidget):

    tempID = 'TEMP'

    currentIDNum = 0

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        window_layout = QHBoxLayout()
        self.setLayout(window_layout)
        # Sets a horizontal layout for the window itself

        ### Enrolling Players Section ###
        
        add_player_layout = QVBoxLayout()

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

        # FINISH MAKING THIS LOOK GOOD

        ### Misc Window Settings ###

        window_layout.addLayout(add_player_layout)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Tournament Name')

        self.playerFirstName.setFocus(True)
        self.show()

    def addPlayer(self):

        pass

        # This will add the player to the table widget

    def clear(self):

        self.playerFirstName.setText('')
        self.playerLastName.setText('')

        self.playerFirstName.setFocus(True)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    enroll = EnrollPlayers()
    sys.exit(app.exec_())
