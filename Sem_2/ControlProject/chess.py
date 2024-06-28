import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QGridLayout,
    QDialog,
    QSizePolicy,
    QSpacerItem,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent


# класс ячейки, содержащий координаты и содержимое ячейки
class Cell:
    def __init__(self, x: int, y: int, content: str = "0"):
        self.x = x
        self.y = y
        self.content = content

    def __repr__(self):
        return self.content


# класс фигуры, содержащий возможные ходы и методы для размещения фигур
class Piece:
    MOVES = {
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
    }

    @staticmethod
    def get_moves(x: int, y: int) -> set[tuple[int, int]]:
        moves = {
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
            (x - 2, y - 1),
            (x - 2, y + 1),
            (x - 1, y - 2),
            (x - 1, y + 2),
            (x + 1, y - 2),
            (x + 1, y + 2),
            (x + 2, y - 1),
            (x + 2, y + 1),
        }
        return moves

    # метод для размещения фигуры на доске
    @staticmethod
    def place_piece(x: int, y: int, board: "Board", is_user: bool):
        content = "U" if is_user else "#"
        board.cells[x][y].content = content
        for dx, dy in Piece.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.cells[nx][ny].content == "0":
                    board.cells[nx][ny].content = "*"


# класс доски, содержащий ячейки и методы для их отображения
class Board:
    def __init__(self, size: int):
        self.size = size
        self.cells = [[Cell(x, y) for y in range(size)] for x in range(size)]

    # метод для очистки доски
    def clear(self):
        self.cells = [[Cell(x, y) for y in range(self.size)] for x in range(self.size)]

    # метод для отображения доски в консоли
    def display(self):
        for row in self.cells:
            print(" ".join(str(cell) for cell in row))


# класс для логики игры
class ChessLogic:
    # метод для проверки корректности позиции
    @staticmethod
    def is_valid_position(posed_figures: set[tuple[int, int]], N: int) -> bool:
        for x, y in posed_figures:
            for move in Piece.get_moves(x, y):
                if move in posed_figures:
                    return False
        return True

    # рекурсивный метод для поиска всех возможных расстановок фигур
    @staticmethod
    def recursion_for_all_arrangements(
        N: int,
        L: int,
        solutions: set[frozenset],
        posed_figures: set[tuple[int, int]],
        x: int,
        y: int,
        count: int,
    ):
        if count == L:
            solutions.add(frozenset(posed_figures))
            return

        for i in range(x, N):
            for j in range(y if i == x else 0, N):
                if (i, j) not in posed_figures and ChessLogic.is_valid_position(
                    posed_figures | {(i, j)}, N
                ):
                    new_posed_figures = posed_figures | {(i, j)}
                    ChessLogic.recursion_for_all_arrangements(
                        N, L, solutions, new_posed_figures, i, j + 1, count + 1
                    )

    # метод для создания доски с фигурами
    @staticmethod
    def create_board(
        size: int, posed_figures: list[tuple[int, int]], is_user: bool
    ) -> Board:
        board = Board(size)
        for x, y in posed_figures:
            Piece.place_piece(x, y, board, is_user)
        return board


# класс диалогового окна для ввода координат
class InputDialog(QDialog):
    def __init__(self, N: int, L: int, K: int):
        super().__init__()
        self.setWindowTitle("Ввод координат")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.N = N
        self.L = L
        self.K = K

        self.board_layout = QGridLayout()
        self.board = Board(N)
        self.user_figures = set()

        for i in range(N):
            for j in range(N):
                label = QLabel()
                label.setStyleSheet(
                    "background-color: white; border: 1px solid black; min-width: 20px; min-height: 20px;"
                )
                label.setAlignment(Qt.AlignCenter)
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.mousePressEvent = lambda event, x=i, y=j: self.handle_click(
                    event, x, y
                )
                self.board_layout.addWidget(label, i, j)

        self.layout.addLayout(self.board_layout)

        self.generate_button = QPushButton("Сгенерировать доску")
        self.generate_button.clicked.connect(self.validate_and_generate_board)
        self.layout.addWidget(self.generate_button)

        self.solutions_label = QLabel("")
        self.layout.addWidget(self.solutions_label)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        self.setLayout(self.layout)

    # метод для обработки клика по ячейке
    def handle_click(self, event: QMouseEvent, x: int, y: int):
        if event.button() == Qt.LeftButton:
            if (x, y) not in self.user_figures and ChessLogic.is_valid_position(
                self.user_figures | {(x, y)}, self.N
            ):
                self.user_figures.add((x, y))
                self.update_board_display()
        elif event.button() == Qt.RightButton and (x, y) in self.user_figures:
            self.user_figures.remove((x, y))
            self.update_board_display()

    # метод для обновления отображения доски
    def update_board_display(self):
        self.board.clear()
        for x, y in self.user_figures:
            Piece.place_piece(x, y, self.board, True)

        for i in range(self.N):
            for j in range(self.N):
                label = self.board_layout.itemAtPosition(i, j).widget()
                cell_content = self.board.cells[i][j].content
                if cell_content == "U":
                    label.setStyleSheet(
                        "background-color: yellow; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                elif cell_content == "*":
                    label.setStyleSheet(
                        "background-color: red; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                else:
                    label.setStyleSheet(
                        "background-color: white; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )

    # метод для проверки корректности ввода и генерации доски
    def validate_and_generate_board(self):
        if not ChessLogic.is_valid_position(self.user_figures, self.N):
            self.display_error("Некорректное расположение фигур")
            return False

        self.generate_board()
        return True

    # метод для генерации доски
    def generate_board(self):
        solutions = set()
        ChessLogic.recursion_for_all_arrangements(
            self.N, self.L, solutions, self.user_figures, 0, 0, 0
        )

        if solutions:
            solution = next(iter(solutions))
            self.show_solution_dialog(Board(self.N), solution, solutions)
        else:
            self.display_error("Решений не найдено")

    # метод для отображения сообщения об ошибке
    def display_error(self, message: str):
        QMessageBox.critical(self, "Ошибка", message)

    # метод для отображения итоговой доски
    def show_solution_dialog(
        self, board: Board, solution: set[tuple[int, int]], solutions: set[frozenset]
    ):
        dialog = SolutionDialog(board, self.user_figures, solution, solutions)
        dialog.exec()


# класс диалогового окна для отображения итоговой доски
class SolutionDialog(QDialog):
    def __init__(
        self,
        board: Board,
        user_figures: set[tuple[int, int]],
        solution: set[tuple[int, int]],
        solutions: set[frozenset],
    ):
        super().__init__()
        self.setWindowTitle("Итоговая доска")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()

        self.board_layout = QGridLayout()

        # размещаем фигуры пользователя на доске
        for x, y in user_figures:
            Piece.place_piece(x, y, board, True)
        # размещаем фигуры алгоритма на доске
        for x, y in solution:
            Piece.place_piece(x, y, board, False)

        # отображаем доску с выделением отличий
        for i in range(board.size):
            for j in range(board.size):
                label = QLabel()
                cell_content = board.cells[i][j].content
                if (i, j) in user_figures:
                    label.setStyleSheet(
                        "background-color: yellow; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                elif cell_content == "#":
                    label.setStyleSheet(
                        "background-color: blue; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                elif cell_content == "*":
                    label.setStyleSheet(
                        "background-color: red; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                else:
                    label.setStyleSheet(
                        "background-color: white; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                label.setAlignment(Qt.AlignCenter)
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.board_layout.addWidget(label, i, j)

        self.layout.addLayout(self.board_layout)

        self.solutions_label = QLabel(f"Количество решений: {len(solutions)}")
        self.layout.addWidget(self.solutions_label)

        self.setLayout(self.layout)
        self.write_solutions_to_file(solutions)

    # запись решений в output.txt
    def write_solutions_to_file(self, solutions):
        with open("output.txt", "w") as file:
            for solution in solutions:
                line = " ".join(f"({x},{y})" for x, y in solution)
                file.write(line + "\n")


# класс основного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расстановка фигур")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.n_input = QLineEdit()
        self.l_input = QLineEdit()

        self.n_label = QLabel("Размер доски:")
        self.l_label = QLabel("Количество фигур:")

        self.layout.addWidget(self.n_label)
        self.layout.addWidget(self.n_input)
        self.layout.addWidget(self.l_label)
        self.layout.addWidget(self.l_input)

        self.generate_button = QPushButton("Далее")
        self.generate_button.clicked.connect(self.open_input_dialog)
        self.layout.addWidget(self.generate_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    # метод для открытия диалогового окна ввода координат
    def open_input_dialog(self):
        try:
            N = int(self.n_input.text())
            L = int(self.l_input.text())
            K = 0

            if N <= 0 or L <= 0 or K < 0 or K >= N**2 or L + K > N**2:
                raise ValueError

            dialog = InputDialog(N, L, K)
            dialog.exec()

        except ValueError:
            self.display_error("Некорректный ввод")

    # метод для отображения сообщения об ошибке
    def display_error(self, message: str):
        QMessageBox.critical(self, "Ошибка", message)


# запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
