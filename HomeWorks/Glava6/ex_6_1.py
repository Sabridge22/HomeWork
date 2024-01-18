def f(list1: list[int], list2: list[int]) -> tuple[list[int], list[int], list[int], list[int]]:
    res1, res2 = [], []
    res3 = list1.copy()
    res4 = list2.copy()

    for i in list1:
        if i in list2:
            res1.append(i)
            res3.remove(i)
        else:
            res2.append(i)

    for j in list2:
        if j in list1:
            res4.remove(j)
        else:
            res2.append(j)

    return res1, res2, res3, res4

if __name__ == '__main__':
    list1 = [0, 33, 37, 6, 10, 44, 13, 47, 16, 18, 22, 25]
    list2 = [1, 38, 48, 8, 41, 7, 12, 47, 16, 40, 20, 23, 25]
    print(f(list1, list2))
