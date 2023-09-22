def para(k, l):
    par = ['()', '[]', '{}']
    if k + l in par: return True
    else: return False




def skob():
    a = input('Введите строку из скобок: ')
    st = []
    for i in a:
        st.append(i)
    i = 0
    cm = len(a)
    while cm > 1:
        k = st[i]
        l = st[i + 1]
        if para(k, l):
            st.pop(i)
    
            st.pop(i)
            i = 0
            cm -= 2
        else:
            i += 1
        if i >= cm:
            print(False)
            break
    if len(st) == 0:
        print(True)



    

    
if __name__ == "__main__":
    skob()
    