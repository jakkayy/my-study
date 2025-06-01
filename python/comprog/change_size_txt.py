txt = input()
txt_list = []
for i in range(len(txt)):
    txt_list.append(txt[i])

ans = ""
for i in range(len(txt_list)):
    if txt_list[i] == " ":
        ans += " "
    if txt_list[i].isupper():
        ans += txt_list[i].lower()
    elif txt_list[i].islower():
        ans += txt_list[i].upper()
print(ans)                   
           
