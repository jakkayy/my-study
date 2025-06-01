chess = {'p':1, 'n':3, 'b':3, 'r':5, 'q':9, 'k':0}
CHESS = {'P':1, 'N':3, 'B':3, 'R':5, 'Q':9, 'K':0}

c_list = []
for i in range(8):
    c = input()
    c_list.append(c)

point = 0
POINT = 0
for j in c_list:
    for k in range(len(j)):
        if j[k] in CHESS:
            POINT += CHESS[j[k]]
        if j[k] in chess:
            point += chess[j[k]]
ans = POINT - point
if ans == 0:
    print('equal')
else:
    print(ans) 
