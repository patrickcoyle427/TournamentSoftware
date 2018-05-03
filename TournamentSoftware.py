#!/usr/bin/python3

# This will contain the switches for each part of the software

from PyQt5.QtWidgets import QApplication

from createNewTournament import *

import sys

class Controller(object):

    def show_new_tournament(self):

        self.createTournament = CreateTournament()
        self.createTournament.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    controller = Controller()
    controller.show_new_tournament()
    sys.exit(app.exec_())

        
