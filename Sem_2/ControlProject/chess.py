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
    QProgressDialog,
)
from PySide6.QtCore import Qt

class ChessLogic:
    @staticmethod
    def matrx_builder(N: int) -> list[list[str]]:  # создание доски
        return [["0" for _ in range(N)] for _ in range(N)]

    @staticmethod
    def piece_moves(
        x: int, y: int
    ) -> set[tuple[int, int]]:  # координаты, которые бьет фигура
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
    def posing_the_figure(
        x: int, y: int, matrix: list[list[str]]
    ) -> list[list[str]]:  # расстановка фигуры на доске
        dragon_moves = [
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
        ]
        matrix[x][y] = "#"
        for i in dragon_moves:
            m, n = i[0], i[1]
            if 0 <= m < len(matrix) and 0 <= n < len(matrix):
                matrix[m][n] = "*"
        return matrix

    @staticmethod
    def create_board(
        matrix: list[list[str]], posed_figures: list[tuple[int, int]]
    ) -> list[list[str]]:  # создание доски с расстановкой фигур
        board = matrix
        for x, y in posed_figures:
            board = ChessLogic.posing_the_figure(x, y, board)
        return board

    @staticmethod
    def recursion_for_all_arrangements(
        N: int,
        L: int,
        solutions: set[frozenset],
        posed_figures: set[tuple[int, int]],
        x: int,
        y: int,
        count: int,
    ):  # находит все возможные расстановки фигур
        if count == L:
            solutions.add(frozenset(posed_figures))
            return

        for i in range(x, N):
            for j in range(y if i == x else 0, N):
                if (i, j) not in posed_figures:
                    new_posed_figures = posed_figures | {(i, j)}
                    ChessLogic.recursion_for_all_arrangements(
                        N, L, solutions, new_posed_figures, i, j + 1, count + 1
                    )

    @staticmethod
    def is_valid_position(
        posed_figures: set[tuple[int, int]], N: int
    ) -> bool:  # проверяет корректность растановок фигур
        for x, y in posed_figures:
            for move in ChessLogic.piece_moves(x, y):
                if move in posed_figures:
                    return False
        return True


class CoordinateInputDialog(QDialog):
    def __init__(self, figure_number: int, N: int):  # окно с вводом координат фигур
        super().__init__()
        self.setWindowTitle(f"Ввод координат для фигуры {figure_number}")
        self.layout = QVBoxLayout()

        self.coord_input = QLineEdit()
        self.coord_label = QLabel(
            f"Введите координаты для фигуры {figure_number} (x y):"
        )
        self.layout.addWidget(self.coord_label)
        self.layout.addWidget(self.coord_input)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def get_coordinates(self) -> tuple[int, int]:  # возвращает введенные координаты
        try:
            x, y = map(int, self.coord_input.text().split())
            return x, y
        except ValueError:
            return None, None


class InputDialog(QDialog):
    def __init__(self, N: int, L: int, K: int):  # расстановка фигур
        super().__init__()
        self.setWindowTitle("Ввод координат")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.N = N
        self.L = L
        self.K = K

        self.coords_inputs = []

        for i in range(K):
            coord_dialog = CoordinateInputDialog(i + 1, N)
            if coord_dialog.exec() == QDialog.Accepted:
                x, y = coord_dialog.get_coordinates()
                if 0 <= x < N and 0 <= y < N:
                    self.coords_inputs.append((x, y))

        self.generate_button = QPushButton("Сгенерировать доску")
        self.generate_button.clicked.connect(self.validate_and_generate_board)
        self.layout.addWidget(self.generate_button)

        self.board_layout = QGridLayout()
        self.layout.addLayout(self.board_layout)

        self.solutions_label = QLabel("")
        self.layout.addWidget(self.solutions_label)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        self.setLayout(self.layout)

    def validate_and_generate_board(
        self,
    ):  # проверка расстановки фигур и генерация доски
        posed_figures = set(self.coords_inputs)
        if not ChessLogic.is_valid_position(posed_figures, self.N):
            self.display_error("Некорректное расположение фигур")
            return False

        self.generate_board()

        return True

    def generate_board(self):  # генерация доски с решением
        posed_figures = set(self.coords_inputs)

        solutions = set()

        ChessLogic.recursion_for_all_arrangements(
            self.N, self.L, solutions, posed_figures, 0, 0, 0
        )

        self.display_board(
            ChessLogic.matrx_builder(self.N),
            next(iter(solutions)) if solutions else None,
        )
        self.solutions_label.setText(f"Количество решений: {len(solutions)}")

    def display_error(self, message: str):  # вызывает окно с ошибкой
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Ошибка")
        error_layout = QVBoxLayout()
        error_label = QLabel(message)
        error_layout.addWidget(error_label)
        error_dialog.setLayout(error_layout)
        error_dialog.exec()

    def display_board(
        self, matrix: list[list[str]], solution: set[tuple[int, int]]
    ):  # отображает доску с расстановкой фигур
        for i in range(self.board_layout.count()):
            self.board_layout.itemAt(i).widget().deleteLater()

        if solution:
            board = ChessLogic.create_board(matrix, solution)
            for i, row in enumerate(board):
                for j, cell in enumerate(row):
                    label = QLabel()
                    color = self.get_color_for_cell(cell, i, j)
                    label.setStyleSheet(
                        f"background-color: {color}; border: 1px solid black; min-width: 15px; min-height: 15px;"
                    )
                    label.setAlignment(Qt.AlignCenter)
                    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    self.board_layout.addWidget(label, i, j)
        else:
            self.display_error("Решений не найдено")

    def get_preplaced_coordinates(
        self,
    ) -> set[tuple[int, int]]:  # координаты расставленных изначально фигур
        return set(self.coords_inputs)

    def get_color_for_cell(
        self, cell: str, x: int, y: int
    ) -> str:  # расскрашивание клеток
        if cell == "#":
            return "blue"
        elif cell == "*":
            return "red"
        else:
            return "white"


class MainWindow(QMainWindow):
    def __init__(self):  # главное окно приложения
        super().__init__()
        self.setWindowTitle("Расстановка фигур")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.n_input = QLineEdit()
        self.l_input = QLineEdit()
        self.k_input = QLineEdit()

        self.n_label = QLabel("Размер доски:")
        self.l_label = QLabel("Количество фигур:")
        self.k_label = QLabel("Количество раставленных фигур:")

        self.layout.addWidget(self.n_label)
        self.layout.addWidget(self.n_input)
        self.layout.addWidget(self.l_label)
        self.layout.addWidget(self.l_input)
        self.layout.addWidget(self.k_label)
        self.layout.addWidget(self.k_input)

        self.generate_button = QPushButton("Далее")
        self.generate_button.clicked.connect(self.open_input_dialog)
        self.layout.addWidget(self.generate_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def open_input_dialog(self):  # ввод координат, проверка и запуск
        try:
            N = int(self.n_input.text())
            L = int(self.l_input.text())
            K = int(self.k_input.text())

            if N <= 0 or L <= 0 or K < 0 or K >= N**2 or L + K > N**2:
                raise ValueError

            dialog = InputDialog(N, L, K)
            dialog.exec()

        except ValueError:
            self.display_error("Некорректный ввод")

    def display_error(self, message: str):  # вывод ошибки
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Ошибка")
        error_layout = QVBoxLayout()
        error_label = QLabel(message)
        error_layout.addWidget(error_label)
        error_dialog.setLayout(error_layout)
        error_dialog.exec()


if __name__ == "__main__":  # запуск  приложения
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
