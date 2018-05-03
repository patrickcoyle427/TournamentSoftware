#!/usr/bin/python3

# TODO:
# Add section to set rounds, or let the software calculate rounds
# Error handling?
# Make it so you can create events with the same name (Maybe create an event number?)

import sys, os

import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QCheckBox, QRadioButton, QLabel,
                             QGridLayout, QLineEdit, QHBoxLayout,
                             QGroupBox, QVBoxLayout)

from PyQt5.QtCore import Qt

class CreateTournament(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        window_layout = QVBoxLayout()
        self.setLayout(window_layout)

        #layout = QGridLayout()
        #self.setLayout(layout)
        # Sets up a grid layout for the window.

        ### Event Name Section ###

        event_name_layout = QHBoxLayout()

        self.event_name_label = QLabel('Event Name:', self)
        # Creates the label for event name

        self.enter_event_name = QLineEdit()
        # Creates a LineEdit object for the user to enter the event's name

        event_name_layout.addWidget(self.event_name_label)
        event_name_layout.addWidget(self.enter_event_name)

        window_layout.addLayout(event_name_layout)

        ### Tournament Type Section ###

        type_and_games_layout = QHBoxLayout()

        self.tournamentTypeGroup = QGroupBox('Tourament Type:')
        # Creates a group of radio button. This one is for the tournament type
        
        self.tournament_type = (QRadioButton('Swiss'), QRadioButton('Single Elimination'))
        # Tuple of the different types of tournaments
        self.tournament_type[0].setChecked(True)
        # Sets 'Swiss' to be checked by default

        tournament_type_layout = QVBoxLayout()
        tournament_type_layout.addWidget(self.tournament_type[0])
        tournament_type_layout.addWidget(self.tournament_type[1])

        self.tournamentTypeGroup.setLayout(tournament_type_layout)

        type_and_games_layout.addWidget(self.tournamentTypeGroup)

        ### Games Played Section ###

        self.gamesPlayedGroup = QGroupBox('Games In Match:')

        self.games_played = (QRadioButton('Best of 1'), QRadioButton('Best of 3'))

        # In a tuple together for organization purposes

        games_played_layout = QVBoxLayout()
        games_played_layout.addWidget(self.games_played[0])
        games_played_layout.addWidget(self.games_played[1])

        self.games_played[0].setChecked(True)

        self.gamesPlayedGroup.setLayout(games_played_layout)

        type_and_games_layout.addWidget(self.gamesPlayedGroup)

        #window_layout.addLayout(type_and_games_layout)

        ### Create Draft Pods Section ###

        self.draftPodGroup = QGroupBox('Draft Pods:')

        self.create_draft_pods = QCheckBox('Create Draft Pods')
        self.create_draft_pods.stateChanged.connect(self.draft_settings)
        
        self.play_in_pods = QCheckBox('Play Within Pods')
        self.play_in_pods.setEnabled(False)

        draft_pod_layout = QVBoxLayout()
        draft_pod_layout.addWidget(self.create_draft_pods)
        draft_pod_layout.addWidget(self.play_in_pods)

        self.draftPodGroup.setLayout(draft_pod_layout)

        type_and_games_layout.addWidget(self.draftPodGroup)

        window_layout.addLayout(type_and_games_layout)

        ### Create Tournament and Cancel Section ###

        buttons = QHBoxLayout()

        self.create_event = QPushButton('Create Event', self)
        self.cancel = QPushButton('Cancel', self)

        #self.create_event.clicked.connect(self.test)
        self.create_event.clicked.connect(self.write_tournament_xml_file)
        self.cancel.clicked.connect(self.close)

        self.create_event.setStyleSheet('background-color: green; color: white')
        self.cancel.setStyleSheet('background-color: red; color: white')

        buttons.addWidget(self.create_event)
        buttons.addWidget(self.cancel)

        window_layout.addLayout(buttons)
        

        self.setWindowTitle('Create New Tournament')
        self.setGeometry(300, 300, 150, 150)
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

    def test(self):

        print('success')

    def write_tournament_xml_file(self):

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

        to_write = ET.ElementTree(tournament_file)

        path = os.path.join(tournament_directory, '{}.xml'.format(self.enter_event_name.text()))

        to_write.write('{}'.format(path),
                             encoding = 'utf-8',
                             xml_declaration = True)
        # Writes the xml file

        self.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    createTournament = CreateTournament()
    sys.exit(app.exec_())
