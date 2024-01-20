def f(list1: list[int], list2: list[int]) -> tuple[list[int], list[int], list[int], list[int]]: # ф-ция для сравнения 2-х списков
    set1 = set(list1)
    set2 = set(list2)

    union_elements = set1.intersection(set2)
    # делаем через 3 for, чтобы сложность была линейной
    res1 = list(union_elements)
    res2 = [x for x in list1 + list2 if x not in union_elements]
    res3 = [x for x in list1 if x not in union_elements]
    res4 = [x for x in list2 if x not in union_elements]

    return res1, res2, res3, res4

if __name__ == '__main__':
    list1 = [0, 33, 37, 6, 10, 44, 13, 47, 16, 18, 22, 25]
    list2 = [1, 38, 48, 8, 41, 7, 12, 47, 16, 40, 20, 23, 25]
    print(f(list1, list2))