def lenA(n: int) -> int: # функция находит длину числа
    k = 1
    cnt = 0
    while k < n:
        k *= 10
        cnt += 1
    return cnt

def Left(n: int, ln: int) -> int: # функция находит первое число
    n = abs(n) // (10 ** (ln - 1))
    return n

def Right(n: int) -> int: # функция находит последнее число
    n = abs(n) % 10
    return n

def pos(n: int) -> int: # функция срезает последнее число
    n = abs(n) // 10
    return n

def per(n: int, ln: int) -> int: # функция срезает первое число
    n = abs(n) % (10 ** (ln-1))
    return n

if __name__ == "__main__":
    a = int(input('Введи число для проверки на полигональность: '))
    ln = lenA(a)
    flag = True
    while ln >= 2:
        if Left(a, ln) == Right(a):
            a = pos(a)
            ln -= 1
            a = per(a, ln)
            ln -= 1
        else:
            flag = False
            break
    print(flag)