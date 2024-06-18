import json
import random
import sys
from tkinter.messagebox import showerror 
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QHBoxLayout, QCheckBox
from PySide6.QtCore import Qt, QTimer

class Snake:
    def __init__(self, startPosition, mapSize, mainWindow, direction="right"):
        self.positions = [startPosition]
        self.length = 1
        self.direction = direction
        self.mapSize = mapSize
        self.mainWindow = mainWindow

    def move(self):
        x, y = self.positions[0]
        
        if self.direction == "right":
            newHead = (x, y + 1)
        elif self.direction == "left":
            newHead = (x, y - 1)
        elif self.direction == "up":
            newHead = (x - 1, y)
        elif self.direction == "down":
            newHead = (x + 1, y)
        
        if newHead not in self.positions:
            self.positions.insert(0, newHead)
            self.positions.pop()
        else:
            self.mainWindow.gameOver("you kill self")
        
        if self.checkIfOutOfBounds(newHead):
            self.mainWindow.gameOver("you go out of bounds")

        if list(newHead) in self.mainWindow.obstacles:
            self.mainWindow.gameOver("you hit an obstacle")

    def checkIfOutOfBounds(self, newHead):
        if newHead[0] < 0 or newHead[0] >= self.mapSize[0] or newHead[1] < 0 or newHead[1] >= self.mapSize[1]:
            return True
        else:
            return False
    
    def changeDirection(self, newDirection):
        if newDirection == "right" and self.direction != "left":
            self.direction = "right"
        elif newDirection == "left" and self.direction != "right":
            self.direction = "left"
        elif newDirection == "down" and self.direction != "up":
            self.direction = "down"
        elif newDirection == "up" and self.direction != "down":
            self.direction = "up"

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
            
            startPosition = self.getStartPosition()
            self.snake = Snake(startPosition, self.mapSize, self, direction = "right")
    
            self.updateSnakePosition()

            self.timer = QTimer()
            self.timer.timeout.connect(self.updateGame)
            self.timer.start(300)

    def gameOver(self, cause):
        self.gameStarted = False
        self.startBtn.show()
        self.squareBlocksBtn.show()
        self.pointsLabel.setText(f"Points: {self.points}")
        self.levelLabel.setText(f"Level: {self.currentLevel}")
        showerror(cause, f"Your points: {self.points}")
        self.timer.stop()

    def generateMap(self):
        map = self.mapsData["maps"][self.currentLevel - 1]
        self.mapSize = map["size"]
        self.obstacles = map["obstacles"]

        if self.squareBlocks:
            widthUnit, heightUnit = ((self.height() - 50) / self.mapSize[0], (self.height() - 50) / self.mapSize[0])
        else:
            widthUnit, heightUnit = ((self.width() - 50) / self.mapSize[1]), ((self.height() - 50) / self.mapSize[0])
        
        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                mapBlock = QLabel()
                mapBlock.setFixedSize(widthUnit, heightUnit)
                mapBlock.setStyleSheet("background-color: #ffffff; color: #000000; border: 2px solid #968986; font-size: 25px; font-weight: semibold;")
                self.gridLayout.addWidget(mapBlock, row, col)

        for obstacle in self.obstacles:
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
    
    def getStartPosition(self):
        availablePositions = []
        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                if [row, col] not in self.obstacles:
                    availablePositions.append((row,col))
        if availablePositions:
            return random.choice(availablePositions)
        else:
            showerror("No available positions")
            
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self.gameStarted:
            key = event.key()
            if key == Qt.Key_A:
                self.snake.changeDirection("left")
            elif key == Qt.Key_D:
                self.snake.changeDirection("right")
            elif key == Qt.Key_W:
                self.snake.changeDirection("up")
            elif key == Qt.Key_S:
                self.snake.changeDirection("down")
            self.updateSnakePosition()
    
    def updateGame(self):
        self.snake.move()
        self.updateSnakePosition()

    def updateSnakePosition(self):

        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                
                if [row, col] not in self.obstacles:
                    mapBlock = self.gridLayout.itemAtPosition(row, col).widget()
                    mapBlock.setStyleSheet("background-color: #ffffff; color: #000000; border: 2px solid #968986; font-size: 25px; font-weight: semibold;")

        for pos in self.snake.positions:
            row, col = pos
            mapBlock = self.gridLayout.itemAtPosition(row, col).widget()
            mapBlock.setStyleSheet("background-color: #ffffff;")

        headPos = self.snake.positions[0]
        row,col = headPos
        mapBlock = self.gridLayout.itemAtPosition(row, col).widget()
        mapBlock.setStyleSheet
        mapBlock.setStyleSheet("background-color: #00ff00;")
    
        for pos in self.snake.positions[:1]:
            row,col = pos
            mapBlock = self.gridLayout.itemAtPosition(row, col).widget()
            mapBlock.setStyleSheet("background-color: #00ff00;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())