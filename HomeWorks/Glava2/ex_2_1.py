def naib() -> None:
    a = input('Введите строку: ')

    left = 0
    right = 0
    max_len = 0

    glass = {}

    while right < len(a):
        if a[right] not in glass or glass[a[right]] < left:
            glass[a[right]] = right
            right += 1
        else:
            left = glass[a[right]] + 1

        max_len = max(max_len, right - left)

    print(a[left:left + max_len])

if __name__ == "__main__":
    naib()