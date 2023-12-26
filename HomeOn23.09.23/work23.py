def prov(a):
    st = []
    for i in a:
        st.append(i)
    ob = 0
    ku = 0
    sc = 0
    flag = True
    for i in range(len(a)):
        if a[i] == '(': ob += 1
        elif a[i] == ')': ob -= 1
        elif a[i] == '{': ku += 1
        elif a[i] == '}': ku -= 1
        elif a[i] == '[': sc += 1
        elif a[i] == ']': sc -= 1
        if (ob < 0) or (ku < 0) or (sc < 0):
            flag = False
            break

    if (ob != 0) or (ku != 0) or (sc != 0):
        flag = False

    if vnut(a) == False:
        flag = False

    return flag

def vnut(a):
    fl = True
    for i in range(len(a) - 1):
        if (a[i] == '{') and ((a[i + 1] == ']') or (a[i + 1] == ')')): fl = False
        if (a[i] == '[') and ((a[i + 1] == '}') or (a[i + 1] == ')')): fl = False
        if (a[i] == '(') and ((a[i + 1] == ']') or (a[i + 1] == '}')): fl = False
    return fl


def naib():
    a = str(input('Введите строку из скобок: '))
    if prov(a):
        return print(True)
    else:
        mmm = ''
        MMM = ''
        ob = 0
        ku = 0
        sc = 0
 
        for n in range(len(a)):
            mmm = ''
            for i in range(n, len(a)):
                if a[i] == '(': ob += 1
                elif a[i] == ')': ob -= 1
                elif a[i] == '{': ku += 1
                elif a[i] == '}': ku -= 1
                elif a[i] == '[': sc += 1
                elif a[i] == ']': sc -= 1
                
                mmm += a[i]

                if prov(mmm):
                    if len(mmm) > len(MMM): MMM = mmm
        if MMM == '':
            return print(False)
        else:
            return print(MMM)

if __name__ == "__main__":
    naib()