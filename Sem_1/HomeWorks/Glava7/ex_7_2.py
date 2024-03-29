def rim(a: str) -> int:
    slov = {'I': 1, 'IV': 4, 'V': 5, 'IX': 9, 'X': 10, 'XL': 40, 'L': 50, 'XC': 90, 'C': 100, 'CD': 400, 'D': 500, 'CM': 900, 'M': 1000}

    b = 0
    i = 0

    while i < len(a):
        if i < len(a) - 1 and a[i:i+2] in slov:
            b += slov[a[i:i+2]]
            i += 2
        else:
            b += slov[a[i]]
            i += 1
    return b

if __name__ == '__main__':
    a = 'MCMXCIV'
    print(rim(a))