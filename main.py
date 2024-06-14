import json
import sys 
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake")
        self.setMinimumSize(500,500)

        self.levelsData = self.loadLevelsData()
        self.mapsData = self.loadMapsData()

        self.currentLevel = 0

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
        self.mainWidget.setStyleSheet("background-color: #E3A89C;")

        layout = QVBoxLayout()

        startBtn = QPushButton("Start")
        startBtn.clicked.connect(self.startGame)
        layout.addWidget(startBtn)

        self.mainWidget.setLayout(layout)

    def startGame(self):
        print("start game")
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())