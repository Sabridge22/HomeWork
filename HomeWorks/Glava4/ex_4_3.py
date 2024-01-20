def group_anagrams(words: list[str]) -> None:
    groups = {}

    for word in words:
        sorted_word_key = tuple(sorted(word))
        if sorted_word_key in groups:
            groups[sorted_word_key].append(word)
        else:
            groups[sorted_word_key] = [word]

    result = list(groups.values())
    print(result)


if __name__ == "__main__":
    words = ['qwe', 'ewq', 'asd', 'dsa', 'dsas', 'qwee', 'zxc', 'cxz', 'xxz', 'z', 's', 'qweasdzxc', 'zzxc']
    group_anagrams(words)