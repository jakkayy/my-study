txt = input()
vowel = ['a','e','i','o','u']
ans = ""
for i in range(len(txt)):
    if txt[i].lower() not in vowel:
        ans += txt[i]
print(ans)
