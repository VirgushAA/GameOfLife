import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPainter, QColor, QResizeEvent
from PyQt6.QtCore import QTimer

CELL_SIZE = 10
WORLD_WIDTH = 300  # Fixed world width in cells
WORLD_HEIGHT = 300  # Fixed world height in cells

class GameOfLife(QWidget):
    def __init__(self):
        super().__init__()
        self.world_grid = np.random.choice([0, 1], size=(WORLD_HEIGHT, WORLD_WIDTH), p=[0.8, 0.2])
        self.grid_width = min(self.width() // CELL_SIZE, WORLD_WIDTH)
        self.grid_height = min(self.height() // CELL_SIZE, WORLD_HEIGHT)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(100)
    
    def update_viewport(self):
        self.grid_width = min(self.width() // CELL_SIZE, WORLD_WIDTH)
        self.grid_height = min(self.height() // CELL_SIZE, WORLD_HEIGHT)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.world_grid[y, x] == 1:
                    painter.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QColor(50, 100, 200))
    
    def resizeEvent(self, event: QResizeEvent):
        self.update_viewport()
        self.update()
    
    def update_game(self):
        new_grid = np.zeros_like(self.world_grid)
        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                neighbors = self.get_neighbors_count(x, y)
                if self.world_grid[y, x] == 1 and neighbors in [2, 3]:
                    new_grid[y, x] = 1
                elif self.world_grid[y, x] == 0 and neighbors == 3:
                    new_grid[y, x] = 1
        self.world_grid = new_grid
        self.update_viewport()
        self.update()
    
    def get_neighbors_count(self, x, y):
        neighbors = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % WORLD_WIDTH, (y + dy) % WORLD_HEIGHT  # Wrap-around logic
                neighbors += self.world_grid[ny, nx]
        return neighbors

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game of Life")
        self.game = GameOfLife()
        self.setCentralWidget(self.game)
        self.resize(500, 500)  # Default window size

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
