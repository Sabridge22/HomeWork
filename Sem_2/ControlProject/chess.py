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


class Cell: # класс клетки
    def __init__(self, x: int, y: int, content: str = "0"):
        self.x = x
        self.y = y
        self.content = content

    def __repr__(self):
        return self.content


class Piece: # класс фигуры и ее ходов
    MOVES = {
        (-1, -1),(-1, 0),
        (-1, 1),(0, -1),
        (0, 1),(1, -1),
        (1, 0),(1, 1),
        (-2, -1),(-2, 1),
        (-1, -2),(-1, 2),
        (1, -2),(1, 2),
        (2, -1),(2, 1),
    }

    @staticmethod
    def get_moves(
        x: int, y: int
    ) -> set[tuple[int, int]]:  # находит возможные ходы для фигуры
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

    @staticmethod
    def place_piece(x: int, y: int, board: "Board", is_user: bool): # размещает фигуру
        content = "U" if is_user else "#"
        board.cells[x][y].content = content
        for dx, dy in Piece.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if board.cells[nx][ny].content == "0":
                    board.cells[nx][ny].content = "*"


class Board: # класс для доски
    def __init__(self, size: int):
        self.size = size
        self.cells = [[Cell(x, y) for y in range(size)] for x in range(size)]

    def clear(self): # сбрасывает все клетки
        self.cells = [[Cell(x, y) for y in range(self.size)] for x in range(self.size)]

    def display(self): # показывает текущее состояние
        for row in self.cells:
            print(" ".join(str(cell) for cell in row))


class ChessLogic: # класс с логикой и проверкой позиций и генерации решений
    @staticmethod
    def is_valid_position(posed_figures: set[tuple[int, int]], N: int) -> bool: # проверяет допустимость расположения фигуры
        for x, y in posed_figures:
            for move in Piece.get_moves(x, y):
                if move in posed_figures:
                    return False
        return True

    @staticmethod
    def recursion_for_all_arrangements(
        N: int,
        L: int,
        solutions: set[frozenset],
        posed_figures: set[tuple[int, int]],
        x: int,
        y: int,
        count: int,
    ): # находит все решения расстановки фигур
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

    @staticmethod
    def create_board(
        size: int, posed_figures: list[tuple[int, int]], is_user: bool
    ) -> Board: # создает доску с указанными фигурами
        board = Board(size)
        for x, y in posed_figures:
            Piece.place_piece(x, y, board, is_user)
        return board


class InputDialog(QDialog): # Интерфейс. Ввод данных расставленных фигур
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

    def handle_click(self, event: QMouseEvent, x: int, y: int): # обработка клика мыши
        if event.button() == Qt.LeftButton:
            if (x, y) not in self.user_figures and ChessLogic.is_valid_position(
                self.user_figures | {(x, y)}, self.N
            ):
                self.user_figures.add((x, y))
                self.update_board_display()
        elif event.button() == Qt.RightButton and (x, y) in self.user_figures:
            self.user_figures.remove((x, y))
            self.update_board_display()

    def update_board_display(self): # визуализация ввода пользователя
        for i in range(self.N):
            for j in range(self.N):
                label = self.board_layout.itemAtPosition(i, j).widget()
                cell_content = self.board.cells[i][j].content
                if (i, j) in self.user_figures:
                    label.setStyleSheet(
                        "background-color: green; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                elif (i, j) in Piece.get_moves(i, j):
                    label.setStyleSheet(
                        "background-color: pink; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                elif cell_content == "*":
                    label.setStyleSheet(
                        "background-color: red; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                elif cell_content == "#":
                    label.setStyleSheet(
                        "background-color: blue; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                elif cell_content == "U":
                    label.setStyleSheet(
                        "background-color: yellow; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )
                else:
                    label.setStyleSheet(
                        "background-color: white; border: 1px solid black; min-width: 20px; min-height: 20px;"
                    )

    def validate_and_generate_board(self): # проверка и генерация доски с решениями
        if not ChessLogic.is_valid_position(self.user_figures, self.N):
            self.display_error("Некорректное расположение фигур")
            return False

        self.generate_board()
        return True

    def generate_board(self): # генерирует доску с допустимыми решениями на основе введеных пользователем данных
        solutions = set()
        ChessLogic.recursion_for_all_arrangements(
            self.N, self.L, solutions, self.user_figures, 0, 0, 0
        )

        if solutions:
            self.display_board(Board(self.N), next(iter(solutions)), solutions)
        else:
            self.display_error("Решений не найдено")
            self.close()

    def display_error(self, message: str): # отображение об ошибке
        QMessageBox.critical(self, "Ошибка", message)

    def display_board(
        self, board: Board, solution: set[tuple[int, int]], solutions: set[frozenset]
    ): # отображает доску с найденным решением и обновляет метку с количеством решений
        for x, y in solution:
            Piece.place_piece(x, y, board, False)

        for i in range(self.N):
            for j in range(self.N):
                label = self.board_layout.itemAtPosition(i, j).widget()
                cell_content = board.cells[i][j].content
                if (i, j) in self.user_figures:
                    label.setStyleSheet(
                        "background-color: green; border: 1px solid black; min-width: 20px; min-height: 20px;"
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

        self.solutions_label.setText(f"Количество решений: {len(solutions)}")
        self.write_solutions_to_file(solutions)

    def write_solutions_to_file(
        self, solutions
    ):  # записывает найденные решения в файл output.txt
        with open("output.txt", "w") as file:
            for solution in solutions:
                line = " ".join(f"({x},{y})" for x, y in solution)
                file.write(line + "\n")


class MainWindow(QMainWindow): # основное окно приложения, где вводятся размер доски и количество  фигур
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

    def open_input_dialog(self): # открывает окно для ввода размера доски и кол-ва фигур
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

    def display_error(self, message: str): # отображение ошибки
        QMessageBox.critical(self, "Ошибка", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
