import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

# Глобальные константы
SIZE = 7  # Размер игрового поля
CELL_SIZE = 50  # Размер ячейки
PLAYER_1_COLOR = QColor("blue")
PLAYER_2_COLOR = QColor("red")

# Создание игрового поля
def create_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    return board

# Проверка победителя
def check_winner(player, board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == player:
                if i < SIZE - 3 and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player:
                    return True
                if j < SIZE - 3 and board[i][j+1] == player and board[i][j+2] == player and board[i][j+3] == player:
                    return True
                if i < SIZE - 3 and j < SIZE - 3 and board[i+1][j+1] == player and board[i+2][j+2] == player and board[i+3][j+3] == player:
                    return True
                if i > 2 and j < SIZE - 3 and board[i-1][j+1] == player and board[i-2][j+2] == player and board[i-3][j+3] == player:
                    return True
    return False

# Создание окна приложения
class HexagonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hexagon")
        self.setFixedSize(CELL_SIZE * SIZE + 5, CELL_SIZE * SIZE + 120)

        self.board = create_board()
        self.player_turn = 1

        self.create_widgets()

    # Создание виджетов окна
    def create_widgets(self):
        self.game_label = QLabel(self)
        self.game_label.setGeometry(10, 10, CELL_SIZE * SIZE, CELL_SIZE * SIZE)
        self.game_label.mousePressEvent = self.mouse_press_event

        self.reset_button = QPushButton("Перезапустить", self)
        self.reset_button.setGeometry(10, CELL_SIZE * SIZE + 20, 100, 30)
        self.reset_button.clicked.connect(self.reset_game)

        self.rules_button = QPushButton("Правила", self)
        self.rules_button.setGeometry(120, CELL_SIZE * SIZE + 20, 100, 30)
        self.rules_button.clicked.connect(self.show_rules)

        self.quit_button = QPushButton("Выйти", self)
        self.quit_button.setGeometry(230, CELL_SIZE * SIZE + 20, 100, 30)
        self.quit_button.clicked.connect(self.close)

    # Обработчик события отрисовки окна
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for i in range(SIZE):
            for j in range(SIZE):
                x = j * CELL_SIZE
                y = i * CELL_SIZE

                painter.setPen(QPen(Qt.black, 1))
                painter.setBrush(Qt.NoBrush)
                painter.drawRect(x, y, CELL_SIZE, CELL_SIZE)

                if self.board[i][j] == 1:
                    painter.setBrush(PLAYER_1_COLOR)
                    painter.drawEllipse(x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10)
                elif self.board[i][j] == 2:
                    painter.setBrush(PLAYER_2_COLOR)
                    painter.drawEllipse(x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10)

    # Обработчик события клика на игровом поле
    def mouse_press_event(self, event):
        col = event.x() // CELL_SIZE
        row = event.y() // CELL_SIZE
        self.make_move(row, col)

    # Ход игрока
    def make_move(self, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = self.player_turn
            self.update()

            if check_winner(self.player_turn, self.board):
                self.show_winner(self.player_turn)
                return

            self.player_turn = 2 if self.player_turn == 1 else 1

    # Показать победителя
    def show_winner(self, player):
        if player == 1:
            winner = "игрок 1"
        else:
            winner = "игрок 2"

        QMessageBox.information(self, "Победа!", "Победил " + winner)
        self.reset_game()

    # Сброс игры
    def reset_game(self):
        self.board = create_board()
        self.player_turn = 1
        self.update()

    # Показать правила
    def show_rules(self):
        QMessageBox.information(self, "Правила игры", "Правила игры Hexagon:\n\nИграют два игрока, по очереди "
                                                     "ставя фишки в свободные клетки поля. Побеждает "
                                                     "игрок, который соберет 4 своих фишки в ряд "
                                                     "(горизонтально, вертикально или по диагонали).")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    hexagon_app = HexagonApp()
    hexagon_app.show()
    sys.exit(app.exec_())
