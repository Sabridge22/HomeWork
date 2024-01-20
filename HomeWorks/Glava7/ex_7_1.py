def santa(user_list: list) -> set:

    dict = {}

    for item in user_list:
        key = item[0]
        if len(item) > 1:
            value = item[1]
        else:
            value = None
        dict[key] = value
    return dict


if __name__ == '__main__':
    user_list = [["name1 surname1", 12345], ["name2 surname2"], ["name3 surname3", 12354], ["name4 surname4", 12435]]
    print(santa(user_list))
