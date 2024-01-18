def pribliz_sum(N: int, spi: list[int], C: int) -> list[str, tuple[list[int], int]]: # функция, которая находит ближайшую сумму 4-х чисел к определенному числу
    best = None
    best_spis = None
    if N <= 4: return 'no solution'
    for i in range(N):
        for j in range(i+1, N):
            for k in range(j+1, N):
                for l in range(k+1, N):
                    pri = spi[i] + spi[j] + spi[k] + spi[l]
                    if best == None: best = pri
                    if best_spis == None: best_spis = [spi[i], spi[j], spi[k], spi[l]]
                    if pri == C:
                        return [spi[i], spi[j], spi[k], spi[l]], pri

                    else:
                        if abs(C - best) > abs(C - pri):
                            best = pri
                            best_spis = [spi[i], spi[j], spi[k], spi[l]]
    return best, best_spis

if __name__ == '__main__':
    N = 5
    spi = [1, 2, 4, -5, -2]
    C = 1

    print(pribliz_sum(N, spi, C))
