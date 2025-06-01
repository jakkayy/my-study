password = input()
c1 = 0
c2 = 0
c3 = 0
c4 = 0
if 3 <= len(password) <= 20:
    for i in range(len(password)):
        if password[i].isupper():
            c1 += 1
        elif password[i].islower():
            c2 += 1
        elif password[i] in ['0','1','2','3','4','5','6','7','8','9']:
            c3 += 1
        elif password[i].isalpha() == False:
            c4 += 1
    if c1 and c2 and c3 and c4 >=1:
        print("Valid")
    else:
        print("Invalid")
else:
    print("Invalid")
