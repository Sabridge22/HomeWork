def naib(): # ф-ция для опр. наибольшей строки без повторных символов
    a = input('Введите строку: ')
    cnt = a[0]
    itog = cnt
    for i in range(len(a)-1):
        cnt = a[i]
        st = i

        while a[st] != a[st + 1] and (a[st + 1] not in cnt):
            cnt += a[st + 1]
            st += 1
            if len(cnt) > len(itog):
                itog = cnt
            if st >= len(a)-1:
                break
    print(itog)

if __name__ == "__main__":
    naib()