def stolb(sl: str, x: int) -> int: #функция для определения кол-ва столбцов
    ln = len(sl)
    pus = x - 2
    y = 0
    while ln > 0:
        pus = x - 2
        ln -= x
        y += 1
        if ln > 0:
            pus2 = pus
            while pus2 > 0:
                ln -=   1
                y += 1
                pus2 -= 1
    return y

def tabel(x: int, y: int) -> list[list[str]]: #функция для создания пустой таблицы
    table = [['-' for _ in range(y)] for _ in range(x)]
    return table

def zigzag(): #функция для задачи "зигзаг"
    sl = input('Введите слово: ')
    x = int(input('Введите кол-во строк: '))

    if x > 1: #для того, чтобы предотвратить ошибки
        y = stolb(sl, x)
        outp = ''
        xxx = ''
        myTable = tabel(x, y)
        x1 = 1 #строка в таблице для буквы
        y1 = 1 #столбец в таблице для буквы
        myTable[0][0] = sl[0] #ставим первую букву в таблице
        cnt = 1 #счетчик для индекса элемента в строке
        while cnt < (len(sl)): #пока индекс меньше максимально возможного в слове...
            while x1 < x and (cnt < (len(sl))): #проверка на то, не последняя ли это строка(везде проверяется длина счетчика тк важна его величина)
                x1 += 1
                cnt += 1
                myTable[x1-1][y1-1] = sl[cnt-1] #замена определенного символа

            if x1 == x and (cnt < (len(sl))): #если достигнута последняя строка
                while (x1 > 1) and (cnt < (len(sl))): #пока не дойдет до первой строки выполнять условия
                    x1 -= 1
                    y1 += 1
                    cnt +=1
                    myTable[x1-1][y1-1] = sl[cnt-1] #замена определенного символа
        for p in myTable: # создание таблицы
            print(' '.join(p))
        for i in myTable:
            for n in i:
                if n != '-':
                    outp += n
        print('Output: ', outp)

    elif x == 1: # если строка одна просто выводим слово
        print(sl)
    else: # если строк меньше 1 выводит ошибку
        print('Ошибка')

if __name__ == "__main__":
    zigzag()