#!/usr/bin/python3

'''
createNewTournament.py - creates a new tournament, based on user's choices
                         in the GUI. Writes these choices to an XML file
                         that will be used for the rest of the event.
'''

import sys, os, random

import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QCheckBox, QRadioButton, QLabel,
                             QGridLayout, QLineEdit, QHBoxLayout,
                             QGroupBox, QVBoxLayout, QMessageBox)

from PyQt5.QtCore import Qt

class CreateTournament(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        window_layout = QVBoxLayout()
        self.setLayout(window_layout)
        # Sets a vertical layout for the window itself

        ### Event Name Section ###

        event_name_layout = QHBoxLayout()
        # Holds the event name layout

        self.event_name_label = QLabel('Event Name:', self)
        # Creates the label for event name

        self.enter_event_name = QLineEdit()
        # Creates a LineEdit object for the user to enter the event's name

        event_name_layout.addWidget(self.event_name_label)
        event_name_layout.addWidget(self.enter_event_name)
        # Adds the event name to the layout

        window_layout.addLayout(event_name_layout)
        # Adds the event_name_layout to the window

        ### Tournament Type Section ###

        option_layout = QHBoxLayout()
        # Layout Container for the tournament option selections

        self.tournamentTypeGroup = QGroupBox('Tourament Type:')
        # Creates a group of radio button. This one is for the tournament type
        
        self.tournament_type = (QRadioButton('Swiss'), QRadioButton('Single Elimination'))
        # Tuple of the different types of tournaments

        # For reference:
        # self.tournament_type[0] is Swiss Style (no one is auto eliminated)
        # self.tournament_type[1] is single elimination (dropped after loss)
        
        self.tournament_type[0].setChecked(True)
        # Sets 'Swiss' to be checked by default

        tournament_type_layout = QVBoxLayout()

        for tType in self.tournament_type:
            
            tournament_type_layout.addWidget(tType)

        self.tournamentTypeGroup.setLayout(tournament_type_layout)

        option_layout.addWidget(self.tournamentTypeGroup)

        ### Games Played Section ###

        self.gamesPlayedGroup = QGroupBox('Games In Match:')

        self.games_played = (QRadioButton('Best of 1'), QRadioButton('Best of 3'))
        # In a tuple together for organization purposes

        # For reference:
        # self.games_played[0] is Best of 1 (only 1 game in match is played)
        # self.games_played[1] is Best of 3 (best 2 of 3 games for match

        games_played_layout = QVBoxLayout()

        for gPlayed in self.games_played:
            
            games_played_layout.addWidget(gPlayed)

        # Loop to add buttons to the layout. Done this way to save time later
        # if another option needs to be added to games_played

        self.games_played[0].setChecked(True)
        # By default, best of 1 is selected

        self.gamesPlayedGroup.setLayout(games_played_layout)

        option_layout.addWidget(self.gamesPlayedGroup)
        # Adds games played

        ### Create Draft Pods Section ###

        self.draftPodGroup = QGroupBox('Draft Pods:')
        # Creates a container for the draftPodOPtions

        self.create_draft_pods = QCheckBox('Create Draft Pods')
        self.create_draft_pods.stateChanged.connect(self.draft_settings)
        # draft_settings enables the play_in_pods option below.
        
        self.play_in_pods = QCheckBox('Play Within Pods')
        self.play_in_pods.setEnabled(False)
        # Play within pods disabled until the create draft pods option
        # is selected.

        draft_pod_layout = QVBoxLayout()
        draft_pod_layout.addWidget(self.create_draft_pods)
        draft_pod_layout.addWidget(self.play_in_pods)

        self.draftPodGroup.setLayout(draft_pod_layout)

        option_layout.addWidget(self.draftPodGroup)

        window_layout.addLayout(option_layout)

        ### Create Tournament and Cancel Section ###

        buttons = QHBoxLayout()

        # Creates a layout for the buttons

        self.create_event = QPushButton('Create Event', self)
        self.cancel = QPushButton('Cancel', self)

        self.create_event.clicked.connect(self.write_tournament_xml_file)
        self.cancel.clicked.connect(self.close)

        self.create_event.setStyleSheet('background-color: green; color: white')
        self.cancel.setStyleSheet('background-color: red; color: white')

        buttons.addWidget(self.create_event)
        buttons.addWidget(self.cancel)

        window_layout.addLayout(buttons)

        ### Window Options ###
        
        self.setWindowTitle('Create New Tournament')
        self.setFixedSize(400, 175)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # Sets it so the user can only close the window, not minimize or maximize

        self.show()

    def draft_settings(self):

        if self.create_draft_pods.isChecked() == True:

            self.play_in_pods.setEnabled(True)
            self.play_in_pods.toggle()

        else:

            if self.play_in_pods.isChecked() == True:
                self.play_in_pods.toggle()
                
            self.play_in_pods.setEnabled(False)

        # Function to make sure the play within pods option is only avaialable
        # if the user actually wants a draft in the first place.

    def write_tournament_xml_file(self):

        def write_file():

            tournament_file = ET.Element('Tournament')

            # Sets up the tournament's XML file. The program will read this
            # to set up the event, and will write what happens in the event to
            # this file.

            tournamentSetup = ET.SubElement(tournament_file, 'TournamentSetup')

            eventName = ET.SubElement(tournamentSetup, 'EventName')
            eventName.text = self.enter_event_name.text()

            structure = ET.SubElement(tournamentSetup, 'Structure')

            style = ET.SubElement(structure, 'Style')

            if self.tournament_type[0].isChecked() == True:

                style.text = 'Swiss'

            else:

                style.text = 'SingleElimination'

            gamesPlayedInMatch = ET.SubElement(structure, 'GamesPlayedInMatch')

            if self.games_played[0].isChecked() == True:
                
                gamesPlayedInMatch.text = '1'

            else:

                gamesPlayedInMatch.text = '3'

            draftpods = ET.SubElement(structure, 'DraftPods')

            if self.create_draft_pods.isChecked() == True:

                draftpods.text = 'True'

            else:

                draftpods.text = 'False'

            playInPods = ET.SubElement(structure, 'PlayInPods')

            if self.play_in_pods.isChecked() == True:

                playInPods.text = 'True'

            else:

                playInPods.text = 'False'

            players = ET.SubElement(tournament_file, 'Players')
            rounds = ET.SubElement(tournament_file, 'Rounds')

            # The create tournament screen pre-writes the players and rounds
            # subelements. These will be used during player enrollment and
            # the creation of rounds respectively

            tournament_directory = 'Tournaments'

            if not os.path.isdir(tournament_directory):

                os.mkdir(tournament_directory)
                
            # Creates the Tournaments directory if it does not exist.
            # Tournaments will all be written to this folder.

            idNumber = str(random.randint(1000000, 9999999))
            # Creates a large random ID number to help prevent the user
            # from accidently creating an event with the same name as an
            # existing one and writing over the old one.

            path = os.path.join(tournament_directory,
                                '{} ID{}.xml'.format(self.enter_event_name.text(),
                                                       idNumber))

            # Builds the path and file name to the tournament file

            while os.path.exists(path):

                idNumber = str(random.randint(1000000, 9999999))
                # If a tournament with the same name AND ID number exist,
                # the ID number is rerolled until it finds one not in use.

                path = os.path.join(tournament_directory,
                                    '{} (ID{}).xml'.format(self.enter_event_name.text(),
                                                           idNumber))

            setIdNumber = ET.SubElement(tournamentSetup, 'IDNumber')
            setIdNumber.text = idNumber
            # Saves the ID number to the file.

            to_write = ET.ElementTree(tournament_file)

            to_write.write('{}'.format(path),
                                 encoding = 'utf-8',
                                 xml_declaration = True)
            # Writes the tournament file

            self.close()
            # Closes the event creation screen once it is done.

        if self.enter_event_name.text().strip() == '':

            # Check to make sure tournament name isn't blank or a bunch
            # of spaces. Displays an error message and prevents the event from being written

            error = QMessageBox()
            error.setIcon(QMessageBox.Information)
            error.setText('No Tournament Name Set')
            error.setWindowTitle('Error')

            self.enter_event_name.setText('')

            self.enter_event_name.setFocus()

            error.exec_()

        else:

            write_file()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    createTournament = CreateTournament()
    sys.exit(app.exec_())
