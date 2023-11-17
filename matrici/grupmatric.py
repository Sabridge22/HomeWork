def f(a):
    itog = []
    
    i = 0
    lenght = len(a)
    while i < lenght:
        itog.append([a[i]])
        n = i + 1
        while n < lenght:
            if sorted(a[n]) == sorted(a[i]):
                itog[i].append(a[n])
                a.remove(a[n])
                lenght -= 1
            n += 1
        i += 1

    print(itog)


if __name__ == '__main__':
    a = ['qwe', 'ewq', 'asd', 'dsa', 'dsas', 'qwee', 'zxc', 'cxz', 'xxz', 'z', 's', 'qweasdzxc', 'zzxc']
    f(a)