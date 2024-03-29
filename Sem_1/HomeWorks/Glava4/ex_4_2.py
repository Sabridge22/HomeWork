from itertools import permutations

def f(nums: list[int]) -> list[list[int]]:
    return [list(p) for p in set(permutations(nums))] # set для избегания повторов

if __name__ == '__main__':
    nums = [1, 2, 3]
    output1 = f(nums)
    print(output1)
