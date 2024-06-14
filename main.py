import json
import sys 
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
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

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.startBtn = QPushButton("start")
        self.startBtn.clicked.connect(self.startGame)
        self.startBtn.setFixedSize(100, 50)
        self.startBtn.setStyleSheet("background-color: #B3A6A3; color: #000000; border: 2px solid #968986; font-size: 25px; font-weight: semibold;")
        layout.addWidget(self.startBtn)

        self.mainWidget.setLayout(layout)

    def startGame(self):
        print("start game")
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())