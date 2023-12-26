def spiral_matrix(matrix):
    result = []
    rows, cols = len(matrix), len(matrix[0])
    row_start, col_start = 0, 0
    row_end, col_end = rows - 1, cols - 1

    while row_start <= row_end and col_start <= col_end:
        # вправо
        for col in range(col_start, col_end + 1):
            result.append(matrix[row_start][col])
        row_start += 1

        # вниз
        for row in range(row_start, row_end + 1):
            result.append(matrix[row][col_end])
        col_end -= 1

        # влево
        if row_start <= row_end:
            for col in range(col_end, col_start - 1, -1):
                result.append(matrix[row_end][col])
            row_end -= 1

        # вправо
        if col_start <= col_end:
            for row in range(row_end, row_start - 1, -1):
                result.append(matrix[row][col_start])
            col_start += 1

    print(result)


if __name__ == '__main__':
    matrix = [
        [1 , 2 , 3 , 4 ],
        [5 , 6 , 7 , 8 ],
        [9 , 10, 11, 12],
        [13, 14, 15, 16],
        [17, 18, 19, 20]
    ]

    spiral_matrix(matrix)
