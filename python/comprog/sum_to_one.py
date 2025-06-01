num = input()
num_list = []
for i in range(len(num)):
    num_list.append(int(num[i]))

answer = 0
while True:
    a = sum(num_list)
    ans = str(a)
    ans_list = []
    if len(ans) == 1:
        answer = ans
        break
    for j in range(len(ans)):
        ans_list.append(int(ans[j]))
    num_list = ans_list
print(answer)
