def matrx_builder(N: int) -> list[list[str]]:
    return [['0' for _ in range(N)] for _ in range(N)]

def piece_moves(x, y):
    moves = {
        (x - 1, y - 1), (x - 1, y),
        (x - 1, y + 1), (x, y - 1),
        (x, y + 1), (x + 1, y - 1),
        (x + 1, y), (x + 1, y + 1),
        (x - 2, y - 1), (x - 2, y + 1),
        (x - 1, y - 2), (x - 1, y + 2),
        (x + 1, y - 2), (x + 1, y + 2),
        (x + 2, y - 1), (x + 2, y + 1)
    }
    return moves

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

def print_board(matrix: list[list[str]]):
    for row in matrix:
        print(" ".join(row))

def recursion_for_all_arrangements(N: int, L: int, solutions: set[tuple[int, int]], solution: set[tuple[int, int]], cnt: int, last_x: int, last_y: int):
    if cnt == L:
        unique_solution = tuple(solution)
        solutions.add(unique_solution)

        # Вывод первого решения
        if len(solutions) == 1:
            print("First solution:")
            print_board(create_board(matrx_builder(N), unique_solution))
        return
    # (last_x, last_y) - координаты последней поставленной фигуры
    for i in range(last_x, N):
        if i == last_x: # если на этой строке уже поставлена фигура, то проход идет начиная с координат последней фигуры
            start_y = last_y
        else: # иначе будет проход всей строки с начала
            start_y = 0
        for j in range(start_y, N):
            if (i, j) not in solution and not piece_moves(i, j).intersection(solution):
                solution.add((i, j))
                recursion_for_all_arrangements(N, L, solutions, solution, cnt + 1, i, j)
                solution.remove((i, j))

if __name__ == "__main__":
    file = open("D:/DzPoPitonu/HomeWork/Laboratory/input.txt", "r")
    N, L, K = map(int, file.readline().split())

    posed_figures = set()
    solutions = set()

    for line in file.readlines():
        x, y = map(int, line.split())
        posed_figures.add((x, y))
    file.close()

    recursion_for_all_arrangements(N, L, solutions, posed_figures, 0, 0, 0)

    print(f"Number of solutions: {len(solutions)}")

    if solutions:
        solutions_str = [" ".join(map(str, solution)) + "\n" for solution in solutions]
        with open("D:/DzPoPitonu/HomeWork/Laboratory/output.txt", "w") as output_file:
            output_file.writelines(solutions_str)
    else:
        print('no solutions')