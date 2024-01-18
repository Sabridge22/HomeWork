def matrx_builder(N: int) -> list[list[str]]:
    return [['0' for _ in range(N)] for _ in range(N)]

def posing_the_figure(x: int, y: int, matrix: list[list[str]]) -> list[list[str]]:
    dragon_moves = [
        (x - 1, y - 1), (x - 1, y),
        (x - 1, y + 1), (x, y - 1),
        (x, y + 1), (x + 1, y - 1),
        (x + 1, y), (x + 1, y + 1),
        (x - 2, y - 1), (x - 2, y + 1),
        (x - 1, y - 2), (x - 1, y + 2),
        (x + 1, y - 2), (x + 1, y + 2),
        (x + 2, y - 1), (x + 2, y + 1)
    ]
    matrix[x][y] = '#'
    for i in dragon_moves:
        m, n = i[0], i[1]
        if 0 <= m < len(matrix) and 0 <= n < len(matrix):
            matrix[m][n] = '*'
    return matrix

def create_board(matrix: list[list[str]], posed_figures: list[tuple[int, int]]) -> list[list[str]]:
    for x, y in posed_figures:
        posing_the_figure(x, y, matrix)
    return matrix

def recursion_for_all_arrangements(N: int, L: int, board: list[list[str]], unique_solutions: set[tuple[int, int]], solution: list[tuple[int, int]],
                                    cnt: int):
    if cnt == L:
        # Базовый случай: достигнуто необходимое количество фигур L
        # Преобразуем кортеж в неизменяемый хешируемый тип (tuple) и добавляем его в множество
        unique_solutions.add(tuple(sorted(solution)))
        return

    for i in range(N):
        for j in range(N):
            # Проверка, что клетка свободна
            if board[i][j] == '0':
                # Создаем копию текущего состояния доски, чтобы не изменять исходную
                new_board = [row[:] for row in board]
                posing_the_figure(i, j, new_board)

                # Рекурсивно вызываем функцию для следующего фрагмента
                recursion_for_all_arrangements(N, L, new_board, unique_solutions, solution + [(i, j)], cnt + 1)

if __name__ == "__main__":
    file = open("D:/DzPoPitonu/HomeWork/Laboratory/input.txt", "r")
    N, L, K = map(int, file.readline().split()) # считывание первой строки и передача значения

    posed_figures = []
    unique_solutions = set()

    for line in file.readlines(): # считывание остальных строк с координатами уже расставленны фигур
        x, y = map(int, line.split())
        posed_figures.append((x, y))
    file.close()
    board = matrx_builder(N) # создание пустой строки

    create_board(board, posed_figures) # расстановка заданных пользователем фигур
    recursion_for_all_arrangements(N, L, board, unique_solutions, posed_figures.copy(), 0) # нахождение всех возможных решений

    print(f"Number of solutions: {len(unique_solutions)}") # вывод в консоль количества найденных решений
    print(board) # вывод в кконсоль начальной позиции
    if unique_solutions: # создание файла и запись в него всех решений
        with open("D:/DzPoPitonu/HomeWork/Laboratory/output.txt", "w") as output_file:
            for solution in unique_solutions:
                output_file.write(" ".join(map(str, solution)) + "\n")
    else: # в случае, когда нет решений
        print('no solutions')
