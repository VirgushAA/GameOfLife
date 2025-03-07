import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer

CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 50, 50

class GameOfLife(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH), p=[0.8, 0.2])
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(100)
        self.setFixedSize(GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y, x] == 1:
                    painter.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QColor(0, 255, 0))
    
    def update_game(self):
        new_grid = np.zeros_like(self.grid)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                neighbors = self.get_neighbors_count(x, y)
                if self.grid[y, x] == 1 and neighbors in [2, 3]:
                    new_grid[y, x] = 1
                elif self.grid[y, x] == 0 and neighbors == 3:
                    new_grid[y, x] = 1
        self.grid = new_grid
        self.update()
    
    def get_neighbors_count(self, x, y):
        neighbors = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT  # Wrap-around logic
                neighbors += self.grid[ny, nx]
        return neighbors

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game of Life")
        self.game = GameOfLife()
        self.setCentralWidget(self.game)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
