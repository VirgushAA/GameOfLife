import sys
import numpy as np
from scipy.ndimage import convolve
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPainter, QColor, QResizeEvent
from PyQt6.QtCore import QTimer, QThread, pyqtSignal

CELL_SIZE = 5
WORLD_WIDTH = 500
WORLD_HEIGHT = 500


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

    class GameThread(QThread):
        updated = pyqtSignal(np.ndarray)

        def __int__(self):
            super().__init__()
            self.grid = None
            self.thread = None

        def set_grid(self, new_grid):
            self.grid = new_grid

        def run(self):
            KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

            neighbor_counts = convolve(self.grid, KERNEL, mode="wrap")

            new_grid = np.zeros_like(self.grid)

            new_grid[(self.grid == 1) & ((neighbor_counts == 2) | (neighbor_counts == 3))] = 1
            new_grid[(self.grid == 0) & (neighbor_counts == 3)] = 1

            self.updated.emit(new_grid)

    def update_game(self):
        self.thread = self.GameThread(self)
        self.thread.updated.connect(self.apply_update)
        self.thread.set_grid(self.world_grid)
        self.thread.start()

    def apply_update(self, new_grid):
        self.world_grid = new_grid
        self.update()

    # def get_neighbors_count(self, x, y):
    #     neighbors = 0
    #     for dy in [-1, 0, 1]:
    #         for dx in [-1, 0, 1]:
    #             if dx == 0 and dy == 0:
    #                 continue
    #             nx, ny = (x + dx) % WORLD_WIDTH, (y + dy) % WORLD_HEIGHT
    #             neighbors += self.world_grid[ny, nx]
    #     return neighbors


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game of Life")
        self.game = GameOfLife()
        self.setCentralWidget(self.game)
        self.resize(500, 500)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
