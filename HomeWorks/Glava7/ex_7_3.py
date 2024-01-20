from itertools import product

def find_combinations(strings: list[str]) -> list[str]:
    # Используем product для создания всех возможных комбинаций символов из строк, список который функция принимает, распоковываем
    combinations = [''.join(combination) for combination in product(*strings)]
    return combinations

def get_pins(pin: str) -> list[str]:
    itog_pin = []
    dict_pin = {'1': '124', '2': '2135', '3': '326', '4': '4157', '5': '52468', '6': '659', '7': '748', '8': '85790', '9': '968', '0': '08'}
    for i in pin:
        j = dict_pin[i]
        itog_pin.append(j) # здесь мы получаем список со вложенными строками из чисел, которые может принимать каждый символ
    return find_combinations(itog_pin) # применяем функцию перебора всех символов всех строк списка


if __name__ == '__main__':
    pin = '812'
    print(get_pins(pin))
