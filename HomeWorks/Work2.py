def Right(n): # функция находит последнее число
    n = abs(n) % 10
    return n

def pos(n): # функция срезает последнее число
    n = abs(n) // 10
    return n

def perevorot(): # функция переворачивает число
    ch = int(input('Введите число: '))
    itog = 0
    if ch < 0: # проверяем на отрицательность и даем флагу значение
        flag = False
    else:
        flag = True
    ch = abs(ch)
    while ch > 0:
        itog = itog * 10 + Right(ch) # составляем число из разрядов
        ch = pos(ch)
    if flag: # возвращаем знак при необходимости
        itog = itog
    else:
        itog = -1 * itog
    if -2**7 <= itog <= 2 ** 7 - 1: # проверка на 8-значность
        return itog
    else:
        return 'no solution'

if __name__ == '__main__':
    print(perevorot())