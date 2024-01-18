def f(a: list[str]) -> None:
    result = []
    for i in range(len(a)):
        result.append([a[i]])
        for n in range(i + 1, len(a)):
            if sorted(a[n]) == sorted(a[i]):
                result[i].append(a[n])

    print(result)

if __name__ == "__main__":
    a = ['qwe', 'ewq', 'asd', 'dsa', 'dsas', 'qwee', 'zxc', 'cxz', 'xxz', 'z', 's', 'qweasdzxc', 'zzxc']
    f(a)
