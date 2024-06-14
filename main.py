import json
import sys 
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake")
        self.setMinimumSize(500,500)

        self.levelsData = self.loadLevelsData()
        self.mapsData = self.loadMapsData()

        self.currentLevel = 0
        self.points = 0

        self.gameStarted = False
        
        self.setupUi()

    def loadLevelsData(self):
        try:
            with open("configs/levels.json", "r") as file:
                return json.load(file)
        except FileNotFoundError as e:
            print(f"error {e}")
            return []
        except json.JSOnDecodeError as e:
            print(f"error {e}")
            return []
        
    def loadMapsData(self):
        try:
            with open("configs/maps.json", "r") as file:
                return json.load(file)
        except FileNotFoundError as e:
            print(f"error {e}")
            return []
        except json.JSOnDecodeError as e:
            print(f"error {e}")
            return []
            
    def resizeEvent(self, event):
        size = event.size()
        width = size.width()
        height = size.height()

        self.mainWidget.setFixedSize(width, height)

        super().resizeEvent(event)

    def setupUi(self):
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setStyleSheet("background-color: #D5B0A8;")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        topRightContainer = QWidget()
        topRightLayout = QHBoxLayout(topRightContainer)
        topRightLayout.setAlignment(Qt.AlignRight)

        self.startBtn = QPushButton("start")
        self.startBtn.clicked.connect(self.startGame)
        self.startBtn.setFixedSize(100, 50)
        self.startBtn.setStyleSheet("background-color: #B3A6A3; color: #000000; border: 2px solid #968986; font-size: 25px; font-weight: semibold;")
        self.layout.addWidget(self.startBtn)

        self.pointsLabel = QLabel()
        self.levelLabel = QLabel()

        topRightLayout.addWidget(self.pointsLabel)
        topRightLayout.addWidget(self.levelLabel)
        self.layout.addWidget(topRightContainer, alignment=Qt.AlignTop | Qt.AlignRight) 

        self.pointsLabel.hide()
        self.levelLabel.hide()

        self.gridLayout = QGridLayout()
        self.layout.addLayout(self.gridLayout)

        self.mainWidget.setLayout(self.layout)

    def startGame(self):
        if not self.gameStarted:
            self.layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
            self.gameStarted = True
            self.startBtn.hide()
            self.pointsLabel.show()
            self.levelLabel.show()
            self.levelLabel.setText(f"Level: {self.currentLevel + 1}")
            self.pointsLabel.setText(f"Points: {self.points}")

        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())