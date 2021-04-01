import sys, os

from functools import partial

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

from backend.queen_solver import *

ERROR_MSG = "ERROR"

class QueenUI(QMainWindow):
    """Queen's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle("Queen Square Solver And Validator")
        self.setFixedSize(600, 800)
        self.gridSize = 8
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.pushButton = QtWidgets.QPushButton(self._centralWidget)
        self.userInput = []
        for i in range(self.gridSize):
            self.userInput.append([0 for j in range(self.gridSize)])

        # Create the display and the buttons
        self._createLabels()
        self._takeinputs()
        self._createButtons()
        self._createBottomButtons()
        self._createResultLabels()

    def on_box_click(self, label):
        row = label // self.gridSize
        column = label % self.gridSize
        self.userInput[row][column] = self.userInput[row][column] + 1
        self.userInput[row][column] %= 3 

    @pyqtSlot()
    def on_submit_click(self):
        result = queen(self.userInput)
        if result == "UNSATISFIABLE":
            resultString = "UNSATISFIABLE"
            self.resultLabel.setText(resultString)
            self.resultLabel.setStyleSheet("color: red;" "font: bold 20px;")
        else:
            for i in range(self.gridSize):
                for j in range(self.gridSize):
                    if self.userInput[i][j] == 0 and result[i][j] == 1:
                        self.buttons[i * self.gridSize + j].setIcon(QIcon(QPixmap("assets/queen_baru.png")))
            self.userInput = result
            resultString = "SATISFIABLE"
            self.resultLabel.setText(resultString)
            self.resultLabel.setStyleSheet("color: green;" "font: bold 20px;")
        
    @pyqtSlot()
    def on_reset_click(self):
        print('PyQt5 button click reset')
        os.execl(sys.executable, sys.executable, *sys.argv)

    def _createResultLabels(self):
        # Rules Label
        self.resultLabel = QtWidgets.QLabel(self._centralWidget)
        self.resultLabel.setGeometry(QtCore.QRect(200, 720, 200, 100))
        self.resultLabel.setText("")

    def _createBottomButtons(self):
        submitButton = QPushButton('Submit', self)
        submitButton.setToolTip('Submit your Queen Square')
        submitButton.move(170,720)
        submitButton.clicked.connect(self.on_submit_click)

        resetButton = QPushButton('Reset', self)
        resetButton.setToolTip('Reset your Queen Square')
        resetButton.move(280,720)
        resetButton.clicked.connect(self.on_reset_click)

    def _createLabels(self):
        # Upper Notice Label
        self.noticeLabel = QtWidgets.QLabel(self._centralWidget)
        self.noticeLabel.setGeometry(QtCore.QRect(20,20, 400, 50))

        # App Title Labels
        self.titleLabel = QtWidgets.QLabel(self._centralWidget)
        self.titleLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setGeometry(QtCore.QRect(100, 80, 400, 50))
        self.titleLabel.setText("N-Queens Solver")
        self.titleLabel.setStyleSheet("color: green;" "font: bold 24px;")

        # Keeping the text of label empty initially.
        self.noticeLabel.setText("")

        # Rules Label
        self.ruleLabel = QtWidgets.QLabel(self._centralWidget)
        self.ruleLabel.setGeometry(QtCore.QRect(20, 630, 500, 100))
        self.ruleLabel.setText("Rules:\n1. Put your queen in the grid\n2. Submit and we can validate and show 1 of the solver for your 8-queen problem\n3. You can block some of the cell if you dont want that cell to be filled by queen")

    def _takeinputs(self):
        self.noticeLabel.setText('Queen Square Succesfully Initialized with\nSize: ' + str(self.gridSize))
        self.pushButton.hide()

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttonsLayout.setSpacing(0)
        # buttonsLayout.setMargin(0)
        # Button text | position on the QGridLayout
        buttons = {}
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                buttons[self.gridSize*i + j] = (i, j)
        
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton("")
            self.buttons[btnText].setFixedSize(50, 50)
            self.buttons[btnText].setIconSize(QSize(40, 40))
            # self.buttons[btnText].setIconSize()
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])

        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)
        # self.generalLayout.setGeometry(QtCore.QRect(20, 650, 500, 500))


# Create a Controller class to connect the GUI and the model
class QueenCtrl:
    """QueensSolver's Controller."""

    def __init__(self, view):
        """Controller initializer."""
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    def _changeIcon(self, btn, btnText):
        """Change image of button."""
        row = btnText // self._view.gridSize
        column = btnText % self._view.gridSize

        if self._view.userInput[row][column] == 0:
            btn.setIcon(QIcon(QPixmap("assets/queen.png")))
        elif self._view.userInput[row][column] == 1:
            btn.setIcon(QIcon(QPixmap("assets/cross.png")))
        else:
            btn.setIcon(QIcon())

        self._view.on_box_click(btnText)


    @pyqtSlot()
    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            btn.clicked.connect(partial(self._changeIcon, btn, btnText))


# Client code
def main():
    """Main function."""
    # Create an instance of `QApplication`
    pycalc = QApplication(sys.argv)

    # Show the Queen's GUI
    view = QueenUI()
    view.show()

    # Create instances of the model and the controller
    QueenCtrl(view=view)
    sys.exit(pycalc.exec_())


if __name__ == "__main__":
    main()
