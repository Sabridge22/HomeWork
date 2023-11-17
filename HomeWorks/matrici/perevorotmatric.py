def mat():

    matrix = [[1 , 2 , 3 , 4 ],
              [5 , 6 , 7 , 8 ],
              [9 , 10, 11, 12],
              [13, 14, 15, 16],
              [17, 18, 19, 20]]

    k = len(matrix[0])
    while len(matrix) < len(matrix[0]): # делаем матрицу "квадратом"
        matrix.append([0]*len(matrix[0]))
    while len(matrix) > len(matrix[0]):
        for i in range(len(matrix)):
            matrix[i].append(0)


    for i in range(len(matrix)):
        for n in range(i, len(matrix)):
            matrix[i][n], matrix[n][i] = matrix[n][i], matrix[i][n]
            if matrix[i][n] == 0:
                matrix[i].remove(0)
    while len(matrix) > k:
        matrix.pop()


    print(matrix)


if __name__ == '__main__':
    mat()
