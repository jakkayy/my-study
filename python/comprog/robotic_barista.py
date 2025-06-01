hot_coffee = {'1':['ESPRESSO',30], '2':['DOUBLE ESPRESSO',35], '3':['HOT AMERICANO',30], '4':["HOT CAFE'LATTE",35], '5':['HOT CAPPUCCINO',35], '6':['HOT MOCCA',40], '7':['HOT CARAMEL LATTE',45], '8':["HOT TAIWANESE TEA CAFE'LATTE",40], '9':['HOT MATCHA LATTE',45], '10':["HOT KOKUTO CAFE'LATTE",35], '11':["HOT THAI TEA CAFE'LATTE",35], '12':['HOT LYCHEE AMERICANO',25]}
ice_coffee = {'1':['ALMOST DIRTY COFFEE',65], '2':['ICED ESPRESSO',45], '3':['ICED AMERICENO',50], '4':['ICED SINGLE ORIGINAL AMERICANO',60], '5':["ICED CAFE'LATTE",40], '6':['ICED CAPPUCCINO',45], '7':['ICED MOCHA',40], '8':["ICED CARAMEL CAFE'LATTE",45], '9':["ICED TAIWANESE TEA CAFE'LATTE",40], '10':["ICED MATCHA CAFE'LATTE",45], '11':["ICED BROWN SUGAR CAFE'LATTE",40], '12':["ICED THAI TEA CAFE'LATTE",45], '13':["ICED LYCHEE AMERICANO",35]}
hot_milk = {'1':['HOT CARAMEL MILK',35], '2':['HOT KOKUTO MILK',40], '3':['HOT COCOA',35], '4':['HOT CARAMEL COCOA',45], '5':['HOT MILK',30]}
ice_milk = {'1':['ICED CARAMEL MILK',], '2':'ICED KOKUTO MILK', '3':'ICED COCOA', '4':'ICED CARAMEL COCOA', '5':'ICED PINK MILK'}
hot_tea = {'1':['HOT GREEN TEA',45], '2':['HOT GINGER TEA',20], '3':['HOT THAI MILK TEA',35], '4':['HOT TAIWANESE TEA',25], }
ice_tea = {'1':['ICED THAI MILK TEA',35], '2':['ICED TAIWANESE MILK',35], '3':['ICED MATCHA LATTE',45], '4':['ICED BROWNSUGAR TEA',40], '5':['ICED LIMEADE TEA',35], '6':['ICED LYCHEE TEA',35], '7':['ICED STRAWBERRY TEA',40], '8':['ICED TEA',30]}
protein_shakes = {'1':['MATCHA PROTEIN SHAKE',55], '2':['CHOCOLATE PROTEIN SHAKE',55], '3':['STRAWBERRY PROTEIN SHAKE',55], '4':['ESPRESSO PROTEIN SHAKE',55], '5':['THAI TEA PROTEIN SHAKE',55], '6':['BROWN SUGAR PROTEIN SHAKE',55], '7':['TAIWANESE TEA PROTEIN SHAKE',55], '8':['CARAMEL PROTEIN SHAKE',55], '9':['PLAIN PROTEIN SHAKE',55], '10':['MILK SHAKE',55]}
soda = {'1':['PEPSI',20], '2':['ICED LIMENADE SODA',20], '3':['ICED LYCHEE SODA',25], '4':['ICED MELON SODA',35], '5':['ICED YUZU SODA',40], '6':['ICED GINGER SODA',25], '7':['ICED UME SODA',25], '8':['ICED STRAWBERRY SODA',40], '9':['ICED SALA SODA',20], '10':['ICED LIME SALA SODA',25]}
smoothie = {'1':['OREO SMOOTHIE VOCANO',60], '2':['COCOA-STRAWBERRY SMOOTHIE',55], '3':['OVALTINE SMOOTHIE',50], '4':['COCOA-OVALTINE SMOOTHIE',60], '5':['STRAWBERRY MILK SMOOTHIE',55], '6':['MELON MILK SMOOTHIE',55], '7':['YUZU MILK SMOOTHIE',55], '8':['LYCHEE MILK SMOOTHIE',55]}
menu = {'1':hot_coffee, '2':ice_coffee, '3':hot_milk, '4':ice_milk, '5':hot_tea, '6':ice_tea, '7':protein_shakes, '8':soda, '9':smoothie }
menu_table = {'1':['hot_coffee'], '2':['ice_coffee'], '3':['hot_milk'], '4':['ice_milk'], '5':['hot_tea'], '6':['ice_tea'], '7':['protein_shakes'], '8':['soda'], '9':['smoothie']}
sweet = {'1':['25 %'],'2':['50 %'],'3':['75 %'],'4':['100 %'],'5':['125 %'],'6':['150 %']}
type_sw = {'1':['Sugar(free)',0], '2':['Honey(+฿5)',5], '3':['sugar 0 cal.(+฿10)',10]}
tc = {'1':['Tube'], '2':['Cap']}
add_on = {'1':['Topping(+฿10)',10],'2':['shot(+฿15)',15]}
def table_drinking(x):
    print(f"{'No.':.4}   {'Menu'.center(38)}price")
    for i in x:
        print(f"{i:>3}.   {x[i][0].center(35)}  {str(x[i][1]).center(4)}")
    print('-'*48)

def table_other(y):
    for j in y:
        print(f"{j}.  {y[j][0]}")
table_other(menu_table)
drink = input('Can you select type of drinking : ')
table_drinking(menu[drink])
coffee = input('Choose menu : ')
price = menu[drink][coffee][1]
if drink in ['1','2','3','4','5','6','9']:
    table_other(type_sw)
    ty_sw = input('Choose type sweet : ')
    table_other(sweet)
    sw = input("Choose your sweetness : ")
    price += type_sw[ty_sw][1]
#add on
add = input("Do you want to add-on?(y/n) : ")
add_list = []
if add == 'y':
    table_other(add_on)
    while True:
        a = input("Can you choose add-on : ")
        if a == "":
            break
        elif a in add_list:
            print("Sorry,you have already choosen!")
        add_list.append(a)
        price += add_on[a][1]
#bill
if drink in ['1','2','3','4','5','6','9']:
    if len(add_list) == 0:
        print(f"Your drink : {menu[drink][coffee][0]}\nType sweet : {type_sw[ty_sw][0]}\nSweet % : {sweet[sw][0]}")
    else:
        print(f"Your drink : {menu[drink][coffee][0]}\nType sweet : {type_sw[ty_sw][0]}\nSweet % : {sweet[sw][0]}\nAdd on : {",".join(add_list)}")
else:
    if len(add_list) == 0:
        print(f"Your drink : {menu[drink][coffee][0]}")
    else:
        print(f"Your drink : {menu[drink][coffee][0]}\nAdd on : {",".join(add_list)}")
print(f"1)confirm{'2)cancel':>20}")
s = input('Select : ')
if s == '1':
    print(f"You have to pay {price} baht, thank you.")
elif s == '2':
    print("You have to cancle order, thank you.")
else:
    while s not in ['1','2']:
        s = input('Select : ')
