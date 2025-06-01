snack = [['Lays',32],['Testo',22],['Cornpup',20],['PR',20],['Twisco',20],['Sunbite',22]]
drinking = [['Meji',13],['Dutchmik',15],['Fourmost',11],['nestle',12]]
food = [['Sandwich',29],['Hamburger',35],['Fried rice',32],['Salad',40]]
all = []
all.extend(snack)
all.extend(drinking)
all.extend(food)
dict_snack, dict_drinking, dict_food = {},{},{}
dict_name_snack, dict_name_drinking, dict_name_food = {},{},{} 
dict_member = {}

def set_dict():
    for i in range(len(snack)):
        dict_snack[str(i+1)] = snack[i][1]
        dict_name_snack[str(i+1)] = snack[i][0]
    
    for j in range(len(drinking)):
        dict_drinking[str(j+1)] = drinking[j][1]
        dict_name_drinking[str(j+1)] = drinking[j][0]
    
    for k in range(len(food)):
        dict_food[str(k+1)] = food[k][1]
        dict_name_food[str(k+1)] = food[k][0]
set_dict()

def MENU():
    print(f"{'MENU'.center(39)}")
    print("========================================")
    print(f"{'SNACKS'.center(40)}")
    print("----------------------------------------")
    for i in range(len(snack)):
        print(f"{i+1}.{snack[i][0]:<35}{snack[i][1]:>2}")
    
    print(f"{'DRINKINGS'.center(40)}")
    print("----------------------------------------")
    for j in range(len(drinking)):
        print(f"{j+1}.{drinking[j][0]:<35}{drinking[j][1]:>2}")
    
    print(f"{'FOODS'.center(40)}")
    print("----------------------------------------")
    for k in range(len(food)):
        print(f"{k+1}.{food[k][0]:<35}{food[k][1]:>2}")
    print("========================================\n")

MENU()

total_order = []

def play(name):
    global all_order
    point_member = 0
    all_order = []
    for i in range(3):
        if i == 0:
            print('Order Snack ! ')
            while True:
                order = input("How your order? : ")
                if order == "":
                    break
                elif order not in dict_snack:
                    print("ERROR")
                    continue
                all_order.append((dict_name_snack[order],dict_snack[order]))
                total_order.append((dict_name_snack[order],dict_snack[order]))
                point_member += dict_snack[order]
        elif i == 1:
            print('Order Drinking ! ')
            while True:
                order = input("How your order? : ")
                if order == "":
                    break
                elif order not in dict_drinking:
                    print("ERROR")
                    continue
                all_order.append((dict_name_drinking[order],dict_drinking[order]))
                total_order.append((dict_name_drinking[order],dict_drinking[order]))
                point_member += dict_drinking[order]
        elif i == 2:
            print('Order Food ! ')
            while True:
                order = input("How your order? : ")
                if order == "":
                    break
                elif order not in dict_food:
                    print("ERROR")
                    continue
                all_order.append((dict_name_food[order],dict_food[order]))
                total_order.append((dict_name_food[order],dict_food[order]))
                point_member += dict_food[order]
    
    total_point = point_member//10
    dict_member[name] = total_point
    
        
    
    def bill():
        print(f"\n{'Total Bill'.center(40)}")
        print("========================================")
        point = 0
        new_all = []
        for j in all_order:
            if j not in new_all:
                new_all.append(j)
            else:
                continue
            
        for i in range(len(new_all)):
            num = all_order.count(new_all[i])
            print(f"{num:>2}  {new_all[i][0]:<33}{(new_all[i][1]*num):>3}")
            point += (all_order[i][1]*num)
        print(f"\nTotal{point:>35}")
        print("----------------------------------------")
        print(f"Member Point{dict_member[name]:>28}\n")
    bill()
    
def total_bill(total_order):
    print(f"\n{'Summary of today'.center(40)}")
    print("========================================")
    new_total_order = []
    for i in total_order:
        if i not in new_total_order:
            new_total_order.append(i)
        else:
            continue
    total_point = 0  
    for j in range(len(new_total_order)):
        c = total_order.count(new_total_order[j])
        print(f"{c:>2}  {new_total_order[j][0]:<33}{(new_total_order[j][1]*c):>3}")
        total_point += new_total_order[j][1]*c
    print(f"\nTotal{total_point:>35}")
    print("----------------------------------------")
    

while True:
    name = input("Welcome to my mart Khun ? ")
    if name != 'close':
        play(name)
    else:
        total_bill(total_order)
        break
