import datetime

menu = [['Espresso',125,140,155],['Matcha',140,155,170],['Cappuccino',135,150,165],['Latte',140,155,170],['Mocha',145,160,175],['Macchiato',150,165,180],['Thai Tea',50,60,65],['Pink Milk',45,55,60],['Bubble Milk Tea',65,75,80],['Cocoa',80,90,95]]
add_on = [['Whipped Cream',20],['Flavor Syrup',35],['Cream milk',15],['Bubble',25]]
dict_menu, dict_add = {},{}
dict_add_price = {}
dict_hot, dict_cold, dict_frappe = {},{},{}
dict_type = {'h':dict_hot,'c':dict_cold,'f':dict_frappe}
dict_hcf = {'h':'Hot','c':'Cold','f':'Frappe'}

def MENU(menu,add_on):
    print('Menu'.center(60))
    print("------------------------------------------------------------")
    print(f"{'NO':>3}.            {'MENU':<15}{'HOT':>3}{'COLD':>13}{'FRAPPE':>13}")
    print("------------------------------------------------------------")
    for i in range(len(menu)):
        print(f"{(i+1):>3}.{menu[i][0].center(27)}{menu[i][1]:>3}{menu[i][2]:>13}{menu[i][3]:>12}")
    print("------------------------------------------------------------\n")
    print(f"{'Add-on'.center(60)}")
    print("------------------------------------------------------------")
    print(f"{'NO'}.{'MENU'.center(30)}{'PRICE':>15}")
    print("------------------------------------------------------------")
    for j in range(len(add_on)):
        print(f"{(j+1):>3}.{add_on[j][0].center(27)}{add_on[j][1]:>16}")
    print("------------------------------------------------------------")
    
MENU(menu,add_on)
    
def set_dict(menu,add_on):
    for i in range(len(menu)):
        dict_menu[str(i+1)] = menu[i][0]
        dict_hot[str(i+1)], dict_cold[str(i+1)] ,dict_frappe[str(i+1)] = menu[i][1], menu[i][2], menu[i][3]
    
    for j in range(len(add_on)):
        dict_add[str(j+1)] = add_on[j][0]
        dict_add_price[str(j+1)] = add_on[j][1]

set_dict(menu,add_on)

class Coffee:
    def __init__(self,coffee_name,type):
        self.coffee_name = coffee_name
        self.type = type
        self.add_on = []
        self.price = 0
    
    def set_add_on(self,add_name,add_price):
        self.add_on.append(add_name)
        self.price += add_price

class Bill:
    def __init__(self,name):
        self.name = name
        self.order = []
        self.cof = []
        self.total = 0
    
    def set_order(self,coffee):
        self.order.append(coffee)
    
    def reciept(self,pay):
        global net_price
        print(f"{'STARBUCKS COFFEE'.center(60)}")
        print(f"{'WELCOME TO STARBUCKS'.center(60)}")
        print(f"{'Central Ladprao'.center(60)}")
        print(f"{'08 0000 0000'.center(60)}")
        print("============================================================") #60
        txt = f"HAVE A GOOD DAY Khun'{self.name}"
        print(f"{txt.center(60)}")
        print("------------------------------------------------------------")

        x = datetime.datetime.now()
        code = 'Chk 0100164524'
        time = x.strftime("%X")
        day = x.strftime("%x")
        print(f"{code}{day:>37} {time:>8}")
        print("------------------------------------------------------------")
        for i in self.order:
            print(f"{i.coffee_name:<53}{float(i.price):>7}")
            self.total += i.price
            for j in i.add_on:
                print(f"> {j}")
            print("\n")
        print(f"\n\n\n\nDiscount{'0.0':>52}")
        print(f"VISA/MC/BBL{float(pay):>49}\n\n")
        print(f"Total{float(self.total):>55}")
        vat = (self.total*7)/100
        net_price = float(self.total)+vat
        def change(pay):
            total = pay - net_price
            return total  
        change_pay = change(pay) 
        print(f"{'Payment'}{float(pay):>53}")
        print(f"{'Vat':>25}{vat:>35}")
        print(f"{'Net':>25}{net_price:>35}")
        print(f"{'Change':>25}{change_pay:>35}\n")
        print("------------------------------------------------------------")

 
def play(name):
    global total_bill,bill
    bill = Bill(name)
    total_bill = Bill(name)
    order = int(input("How many your order? : "))
    for i in range(order):
        while True:
            coffee_name = input("What your coffee name? : ")
            if coffee_name in dict_menu:
                break
            print("ERROR")
        
        while True:
            type = input("What your coffee type? : ")
            if type in dict_type:
                break
            print("ERROR")
        
        coffee = Coffee(dict_menu[coffee_name],dict[type])
        coffee.price += dict_type[type][coffee_name]
        a = []
        while len(a) < len(add_on):
            add = input("What your add_on in coffee? : ")
            if add == "":
                break
            elif add not in a:
                a.append(add)
                coffee.set_add_on(dict_add[add],dict_add_price[add])
            elif add in a:
                print("ERROR")
        bill.set_order(coffee)
        total_bill.set_order(bill)
 
       
while True:
    name = input("Your name? : ")
    if name != 'end':
        play(name)
        pay = int(input("Can you pay now? : "))
        print('\n\n')
        bill.reciept(pay)
    else:
        break
