def pribliz_sum(N: int, spi: list[int], C: int) -> list[str, tuple[list[int], int]]:
    if N <= 4:
        return 'no solution'

    spi.sort()
    best_diff = float('inf') # создание положительной бесконечности(нашел в Интернете)
    best_spis = None

    for i in range(N - 3): # задается таким образом, чтобы осталось 3 свободных "слота"
        for j in range(i + 1, N - 2): # задается так, чтобы была после i и оставалось 2 свободных "слота"
            left = j + 1 # идет после j
            right = N - 1 # всегда последняя буква(индекс последей буквы)

            while left < right:
                current_sum = spi[i] + spi[j] + spi[left] + spi[right]
                current_diff = abs(C - current_sum)

                if current_diff < best_diff:
                    best_diff = current_diff
                    best_spis = [spi[i], spi[j], spi[left], spi[right]]

                if current_sum < C:
                    left += 1
                else:
                    right -= 1

    return sum(best_spis), best_spis

if __name__ == '__main__':
    N = 5
    spi = [1, 2, 4, -5, -2]
    C = 1

    print(pribliz_sum(N, spi, C))