txt = input()

for j in range(len(txt)):
    n = len(txt)
    if j == 0:
        space = " "*((2*(n-1))-(2*j))
        text = txt[0]+" "
        print(space+text)
    else:
        k1 = ""
        for k in range(1,j+1):
            k1 += txt[k]+" "
        k2 = ""
        for h in range(j,0,-1):
            k2 += txt[h]+" "
        space = " "*((2*(n-1))-(2*j))
        print(space+k2+txt[0]+" "+k1)
