from itertools import combinations

def f(spisok: list[str]) -> set[frozenset]: # возвращает подмножества, не содержащих повторяющихся элементов, не включая пустое множество

    a = {frozenset(i) for j in range(1, len(spisok) + 1) for i in combinations(spisok, j)}

    return a
if __name__ == '__main__':
    list1 = ['a', 'b', 'c', 'd', 'd']
    print(f(list1))
