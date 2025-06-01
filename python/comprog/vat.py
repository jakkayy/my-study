n = int(input()) #จำนวนคน
money = []
for i in range(n):
    m = int(input())
    money.append(m)
vat = 0
for j in money:
    if j < 100000:
        vat += 0
    elif 100000 <= j <= 500000:
        vat += j*0.05
    elif 500001 <= j <= 1000000:
        vat += j*0.1
    else:
        vat += j*0.2
print(f"{vat:.2f}")
