import json
import sys 
from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake")
        self.setMinimumSize(500,500)

        self.levelsData = self.loadLevelsData()
        self.mapsData = self.loadMapsData()

        self.setupUi()

    def loadLevelsData(self):
        try:
            with open("configs/levels.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSOnDecodeError:
            return []
        
    def loadMapsData(self):
        try:
            with open("configs/maps.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSOnDecodeError:
            return []
            
    def resizeEvent(self, event):
        size = event.size()
        width = self.width()
        height = self.height()

        super().resizeEvent(event)

    def setupUi(self):
        print(self.levelsData)
        print(self.mapsData)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())