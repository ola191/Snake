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
        
        if list(newHead) not in self.positions:
            self.positions.insert(0, newHead)

            if list(newHead) in self.mainWindow.apples:
                self.mainWindow.apples.remove(list(newHead))
                self.length += 1
                self.mainWindow.points += 1
                self.mainWindow.pointsLabel.setText(f"{self.mainWindow.points}")
            else:
                self.positions.pop()
        else:
            self.mainWindow.gameOver("you kill self")
        
        if self.checkIfOutOfBounds(list(newHead)):
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
        self.apples = []

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
        self.mainWidget.setContentsMargins(10, 10, 10, 10)
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setStyleSheet("background-color: #b3a6a3;")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        topContainer = QWidget()
        topLayout = QHBoxLayout(topContainer)
        topLayout.setContentsMargins(0, 0, 0, 0)

        self.pointsLabel = QLabel(f"{self.points}")
        self.pointsLabel.alignment = Qt.AlignCenter
        self.pointsLabel.setStyleSheet("font-size: 25px; font-weight: semibold;")
        self.levelLabel = QLabel(f"Level: {self.currentLevel}")
        self.levelLabel.hide()
        topLayout.addWidget(self.pointsLabel, alignment=(Qt.AlignCenter))
        # topLayout.addWidget(self.levelLabel, alignment=Qt.AlignLeft)

        self.layout.addWidget(topContainer) 

        self.startBtn = QPushButton("start")
        self.startBtn.clicked.connect(self.startGame)
        self.startBtn.setFixedSize(100, 50)
        self.startBtn.setStyleSheet("background-color: #B3A6A3; color: #000000; border: 2px solid #968986; font-size: 25px; font-weight: semibold;")
        self.startBtn.contentsMargins = (10, 10, 10, 10)
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
            self.gameStarted = True
            
            self.startBtn.hide()
            self.squareBlocksBtn.hide()
            
            self.levelLabel.setText(f"Level: {self.currentLevel}")
            self.pointsLabel.setText(f"{self.points}")

            startPosition = self.getStartPosition()
            self.snake = Snake(startPosition, self.mapSize, self, direction = "right")

            self.generateMap()

            self.generateApples()

            self.updateSnakePosition()

            self.timer = QTimer()
            self.timer.timeout.connect(self.updateGame)
            self.timer.start(self.levelsData["levels"][self.currentLevel]["speed"])

    def gameOver(self, cause):
        self.timer.stop()

        self.gameStarted = False
        self.startBtn.show()
        self.squareBlocksBtn.show()
        self.currentLevel = 0
        self.points = 0
        self.pointsLabel.setText(f"{self.points}")
        self.levelLabel.setText(f"Level: {self.currentLevel}")

        self.clearlayout(self.gridLayout)

    def clearlayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.removeItem(layout.itemAt(i))
            
    def generateMap(self):

        if self.squareBlocks:
            widthUnit, heightUnit = ((self.height() - 50) / self.mapSize[0], (self.height() - 50) / self.mapSize[0])
        else:
            widthUnit, heightUnit = ((self.width() - 50) / self.mapSize[1]), ((self.height() - 50) / self.mapSize[0])
        
        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                item = self.gridLayout.itemAtPosition(row,col)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        self.gridLayout.removeWidget(widget)
                        widget.deleteLater()

        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                mapBlock = QLabel()
                mapBlock.setFixedSize(widthUnit, heightUnit)
                mapBlock.setStyleSheet("background-color: #ffffff; color: #000000; border: 2px solid #968986; font-size: 25px; font-weight: semibold;")
                self.gridLayout.addWidget(mapBlock, row, col)

        for obstacle in self.obstacles:
            item = self.gridLayout.itemAtPosition(obstacle[0], obstacle[1])
            if item is not None:
                widget = item.widget()
                if widget:
                    widget.setStyleSheet("background-color: #000000;")

        self.generateApples()

    def generateApples(self):
        availablePositions = []
        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                if [row, col] not in self.obstacles and [row, col] not in self.snake.positions:
                    availablePositions.append([row, col])
        try:
            applesCount = self.levelsData["levels"][self.currentLevel]["maxLength"]
            print(applesCount)
        except Exception as e:
            return e
        self.apples = random.sample(availablePositions, applesCount)

        for apple in self.apples:
            row, col = apple
            self.gridLayout.itemAtPosition(row,col).widget().setStyleSheet("background-color: #ff0000;")

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
        map = self.mapsData["maps"][self.currentLevel]
        self.mapSize = map["size"]
        self.obstacles = map["obstacles"]
        
        minDistanceFromBorder = 3

        availablePositions = []
        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                if [row, col] not in self.obstacles:
                    if (row >= minDistanceFromBorder and row <= self.mapSize[0] - minDistanceFromBorder) and (col >= minDistanceFromBorder and col <= self.mapSize[1] - minDistanceFromBorder):
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
        if self.gameStarted:
            self.snake.move()
            self.updateSnakePosition()

            if len(self.apples) == 0:
                self.nextLevel()

    def nextLevel(self):
        self.timer.stop()
        self.currentLevel += 1
        if self.currentLevel < len(self.levelsData["levels"]):
            self.points += 10
            self.pointsLabel.setText(f"{self.points}")
            self.levelLabel.setText(f"Level: {self.currentLevel}")
            
            self.gameStarted = False
            
            self.startGame()
        else:
            self.gameOver("You win!")

    def updateSnakePosition(self):
        for row in range(self.mapSize[0]):
            for col in range(self.mapSize[1]):
                item = self.gridLayout.itemAtPosition(row, col)
                if item is not None:
                    mapBlock = item.widget()
                    if mapBlock:
                        if [row, col] not in self.obstacles and [row, col] not in self.snake.positions and [row, col] not in self.apples:
                            mapBlock.setStyleSheet("background-color: #978a87; color: #000000; border: 2px solid #7a7270; font-size: 25px; font-weight: semibold;")

        for pos in self.snake.positions:
            row, col = pos
            item = self.gridLayout.itemAtPosition(row, col)
            if item is not None:
                mapBlock = item.widget()
                mapBlock.setStyleSheet("background-color: #00ff00;")

        for apple in self.apples:
            row, col = apple
            item = self.gridLayout.itemAtPosition(row,col)
            if item is not None:
                mapBlock = item.widget()
                mapBlock = self.gridLayout.itemAtPosition(row, col).widget()
                mapBlock.setStyleSheet("background-color: #ff0000;")

        headPos = self.snake.positions[0]
        row,col = headPos
        item = self.gridLayout.itemAtPosition(row, col)

        if item is not None:
            mapBlock = item.widget()
            mapBlock = self.gridLayout.itemAtPosition(row, col).widget()
            mapBlock.setStyleSheet
            mapBlock.setStyleSheet("background-color: #1eb81e;")
    
        for pos in self.snake.positions[:1]:
            row,col = pos
            item = self.gridLayout.itemAtPosition(row, col)
            if item is not None:
                mapBlock = item.widget()
                mapBlock = self.gridLayout.itemAtPosition(row, col).widget()
                mapBlock.setStyleSheet("background-color: #1eb81e;")

        self.pointsLabel.setText(f"{self.points}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())