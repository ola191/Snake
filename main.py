import json
import sys 
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QHBoxLayout, QCheckBox
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
        self.squareBlocks = True
        
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

        if self.gameStarted:
            self.updateMapBlockSize()

        super().resizeEvent(event)

    def setupUi(self):
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setStyleSheet("background-color: #D5B0A8;")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        topContainer = QWidget()
        topLayout = QHBoxLayout(topContainer)
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSpacing(10)

        self.pointsLabel = QLabel(f"Points: {self.points}")
        self.levelLabel = QLabel(f"Level: {self.currentLevel}")

        topLayout.addWidget(self.pointsLabel, alignment=(Qt.AlignRight))
        topLayout.addWidget(self.levelLabel, alignment=Qt.AlignLeft)

        self.layout.addWidget(topContainer) 

        self.startBtn = QPushButton("start")
        self.startBtn.clicked.connect(self.startGame)
        self.startBtn.setFixedSize(100, 50)
        self.startBtn.setStyleSheet("background-color: #B3A6A3; color: #000000; border: 2px solid #968986; font-size: 25px; font-weight: semibold;")
        self.layout.addWidget(self.startBtn)

        self.squareBlocksBtn = QCheckBox("square blocks")
        self.squareBlocksBtn.setChecked(self.squareBlocks)
        self.squareBlocksBtn.stateChanged.connect(self.toggleSquareBlocks)
        self.layout.addWidget(self.squareBlocksBtn)

        topContainer.setFixedHeight(50)

        self.gridLayout = QGridLayout()
        self.layout.addLayout(self.gridLayout)

        self.mainWidget.setLayout(self.layout)

    def startGame(self):
        if not self.gameStarted:
            self.currentLevel += 1
            self.gameStarted = True
            
            self.startBtn.hide()
            self.squareBlocksBtn.hide()
            
            self.levelLabel.setText(f"Level: {self.currentLevel}")
            self.pointsLabel.setText(f"Points: {self.points}")

            self.generateMap()

    def generateMap(self):
        map = self.mapsData["maps"][self.currentLevel - 1]
        self.mapSize = map["size"]
        obstacles = map["obstacles"]

        if self.squareBlocks:
            print("square blocks")
            widthUnit, heightUnit = ((self.height() - 50) / self.mapSize[0], (self.height() - 50) / self.mapSize[0])
        else:
            print("normal blocks")
            widthUnit, heightUnit = ((self.width() - 50) / self.mapSize[1]), ((self.height() - 50) / self.mapSize[0])
        
        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                mapBlock = QLabel()
                mapBlock.setFixedSize(widthUnit, heightUnit)
                mapBlock.setStyleSheet("background-color: #ffffff; color: #000000; border: 2px solid #968986; font-size: 25px; font-weight: semibold;")
                self.gridLayout.addWidget(mapBlock, row, col)

        for obstacle in obstacles:
            self.gridLayout.itemAtPosition(obstacle[0], obstacle[1]).widget().setStyleSheet("background-color: #000000;")

    def updateMapBlockSize(self):
        if self.squareBlocks:
            widthUnit, heightUnit = ((self.height() - 50) / self.mapSize[0], (self.height() - 50) / self.mapSize[0])
        else:
            widthUnit, heightUnit = ((self.width() - 50) / self.mapSize[1]), ((self.height() - 50) / self.mapSize[0])

        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                mapBlock = self.gridLayout.itemAtPosition(row, col).widget()
                mapBlock.setFixedSize(widthUnit, heightUnit)
    
    def toggleSquareBlocks(self, state):
        if state == self.squareBlocksBtn.isChecked():
            self.squareBlocks = False
        else:
            self.squareBlocks = True
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())