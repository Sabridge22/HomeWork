def pere(): # ф-ция меняющая местами слова
    a = input('Введите строку: ')
    b = ''
    a = a + ' '
    itog = ''
    for i in a:
        if i != ' ':
            b += i
        else:
            itog = b + ' ' + itog
            b = ''

    itog = itog.lstrip()
    itog = itog.rstrip()
    itog = itog.capitalize()

    print(itog)

if __name__ == "__main__":
    pere()