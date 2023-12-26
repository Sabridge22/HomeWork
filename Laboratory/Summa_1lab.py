def sum_of_num(num_list, S, start_sum, final_str, first_num): # функция для расстановки + и - для нахождения определенной суммы
    if len(num_list) == 0:
        if S == start_sum:
            return f'{first_num}{final_str}={S}' # делаем красивый ответ, добавляя первое число и финальную сумму
        else:
            return 'no solution'

    num = num_list[0]
    result1 = sum_of_num(num_list[1:], S, start_sum + num, final_str + "+" + str(num), first_num)
    result2 = sum_of_num(num_list[1:], S, start_sum - num, final_str + "-" + str(num), first_num)
    if result1 != 'no solution':
        return result1
    elif result2 != 'no solution':
        return result2
    else:
        return 'no solution'

if __name__ == "__main__":

    stroka = open('D:/DzPoPitonu/Laboratory/chisla_for_1lab.txt').readline().split() # открытие файла

    N = int(stroka.pop(0))
    S = int(stroka.pop(-1))

    numbers_list = [int(i) for i in stroka]
    first_num = numbers_list.pop(0) # удаляем первое число, чтобы перед ним не стояли знаки +,- и чтобы оно всегда было положительным
    print(sum_of_num(numbers_list, S, first_num, '', first_num)) # сразу закидываем первое число в начальную сумму