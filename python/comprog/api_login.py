import requests
from bs4 import BeautifulSoup


session = requests.Session()

login_url = input('กรอก Link login : ')
res = session.get(login_url)
soup = BeautifulSoup(res.text, 'html.parser')

token_input = soup.find('input', {'name': 'logintoken'})
logintoken = token_input['value'] if token_input else ''
username = input('username : ')
password = input('password : ')

login_data = {
    'username': username, 
    'password': password,
    'logintoken': logintoken
}

res = session.post(login_url, data=login_data)

rounds = int(input('กรอกจำนวนข้อ : '))
quiz_url = input('กรอก link : ')

for i in range(rounds):
    if i == 0: pass
    else: quiz_url += f'&page={i}'
    res = session.get(quiz_url)
    data = BeautifulSoup(res.text, 'html.parser')
    search_correct = data.find('input', {'checked' : 'checked'})
    print(int(search_correct['value'])+1)
