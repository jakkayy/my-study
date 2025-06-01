blue_card_member = {}
fuel_type = {'1':32.97, '2':35.58, '3':35.95, '4':33.84, '5':44.24}
fuel_order = [('diesel',32.97),('gasohol 91',35.58),('gasohol 95',35.95),('e 20',33.84),('benzine',44.24)]
reward = {'35':'Glass PTT', '50':'Cap PTT', '85':'Umbrella PTT', '125':'Folding Table PTT', '200':'Bag PTT', '289':'T-shirt PTT', '399':'Folding Chair PTT'}
rw_point = {'Glass PTT':35, 'Cap PTT':50, 'Umbrella PTT':85, 'Folding Table PTT':125, 'Bag PTT':200, 'T-shirt PTT':289, 'Folding Chair PTT':399}

def table_fuel(fuel_order):
    print(f"{'Fuel Station'.center(33)}")
    print('-'*33)
    print(f" No. |{'Fuel'.center(14)}|{'Price'.center(13)}")
    print('-'*33)
    n = 1
    for i in fuel_order:
        print(f"{str(n).center(3)}. |{i[0].center(14)}|{str(i[1]).center(13)}")
        n += 1
    print('-'*33,'\n')

while True:  
    table_fuel(fuel_order)
    name = input("What is your name? : ")
    if name == 'end':
        break
    add_fuel = input("What do you want to add type fuel? : ")
    if int(add_fuel) not in range(1,len(fuel_type)+1):
        while True:
            add_fuel = input("What do you want to add type fuel? : ")
            if int(add_fuel) in range(1,len(fuel_type)+1):
                break
    amount = int(input("What you want to pay refuel? : "))
    pay = int(input("Request permission to recieve money : "))
    if pay < amount:
        while True:
            more = int(input("Please pay more : "))
            pay += more
            if pay >= amount:
                break
    card = input("Do you have a blue card?(y/n) : ")
    if card == 'n':
        want = input("Do you want to apply for membership?(y/n) : ")
    #add member or add point
    liter = amount/fuel_type[add_fuel]
    point = 0
    if name not in blue_card_member:
        if card == 'y':
            if add_fuel == '1':
                blue_card_member[name] = int(liter)//4
                point = int(liter)//4
            else:
                blue_card_member[name] = int(liter)
                point = int(liter)
        elif want == 'y':
            if add_fuel == '1':
                blue_card_member[name] = int(liter)//4
                point = int(liter)//4
            else:
                blue_card_member[name] = int(liter)
                point = int(liter)//4
        else: pass
    else:
        if card == 'y':
            if add_fuel == '1':
                blue_card_member[name] += int(liter)//4
                point += int(liter)//4
            else:
                blue_card_member[name] += int(liter)
                point += int(liter)
        else: pass
            
    #change money
    change = 0
    if pay > amount :
        change = pay - amount
    elif pay < amount :
        print("Please pay more.")
        more = amount - pay
        pay_new = int(input("Pay more : "))
        all = more - pay_new
        while True:
            if all == 0:
                print("It's complete!")
                break
            if all < 0:
                back = all + amount
                print("It's complete!")
                print(f"You get your money back {back} baht.")
                break
            pay_new = int(input("Pay more : "))
    else:
        change = 0

    #cash back
    cb = 0
    if name not in blue_card_member:
        pass
    elif blue_card_member[name] >= 100:
        check_num = blue_card_member[name]//100
        check = input("Do you want to exchange money?(y/n) : ")
        if check == 'y':
            check_round = int(input(f"You have a total of {check_num} round,how much do you want to exchange? : "))
            cb = check_round*100
            blue_card_member[name] -= cb
        else:
            pass
    else:
        pass
    
    #reward
    rw = ""
    ask = input('Do you want to change reward?(y/n) : ')
    if blue_card_member[name] >= 35:
        can = []
        if ask == 'y':
            for i in reward:
                if blue_card_member[name] >= int(i):
                    can.append(reward[i])
            ans = int(input(f"Can you select {','.join(can)} (you can input number position) : "))
            rw = can[ans-1]
            print(f"Congratulations! you get {rw}")
            blue_card_member[name] -= rw_point[can[ans-1]]
        else:
            print("You don't to change reward")
    elif blue_card_member[name] < 35 and ask == 'y':
        print("Sorry, You can't to change reward because Your point is not enough")
    else:
        print("You don't to change reward")

    #bill
    #refuel every 500 bath,you get water 1.5 L. 1 bottle
    if card == 'y' or want == 'y':
        if ask == 'y':
            if amount >= 500:
                water = amount//500
                print(f"Name : {name}\nAmount : {amount}\nLiter : {liter:.2f}\nPay : {pay}\nChange : {change}\nPoint : {point}")
                print(f"Total member point : {blue_card_member[name]}\nCash back : {cb}\nWater 1.5 L. : {water} bottle")
            else:
                print(f"Name : {name}\nAmount : {amount}\nLiter : {liter:.2f}\nPay : {pay}\nChange : {change}\nPoint : {point}")
                print(f"Total member point : {blue_card_member[name]}\nCash back : {cb}")
        else:
            if amount >= 500:
                water = amount//500
                print(f"Name : {name}\nAmount : {amount}\nLiter : {liter:.2f}\nPay : {pay}\nChange : {change}\nPoint : {point}")
                print(f"Total member point : {blue_card_member[name]}\nCash back : {cb}\nWater 1.5 L. : {water} bottle")
            else:
                print(f"Name : {name}\nAmount : {amount}\nLiter : {liter:.2f}\nPay : {pay}\nChange : {change}\nPoint : {point}")
                print(f"Total member point : {blue_card_member[name]}\nCash back : {cb}")
            
    else:
        if amount >= 500:
            water = amount//500
            print(f"Name : {name}\nAmount : {amount}\nLiter : {liter:.2f}\nPay : {pay}\nChange : {change}\nWater 1.5 L. : {water} bottle")
        else:
            print(f"Name : {name}\nAmount : {amount}\nLiter : {liter:.2f}\nPay : {pay}\nChange : {change}")
    
