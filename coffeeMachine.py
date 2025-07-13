#coffee machine
from time import sleep

machine_power = True

resource={
    "Water": 300,
    "Milk": 200,
    "Coffee": 100,
    "Money": 0,

}

menu={
    "espresso":{
        "Water": 50,
        "Milk": 0,
        "Coffee":18,
        "Cost":2
    },
    "latte":{
        "Water": 200,
        "Milk": 150,
        "Coffee": 24,
        "Cost":3
    },
    "cappuccino":{
        "Water": 250,
        "Milk": 100,
        "Coffee": 24,
        "Cost":4
    }
}

def check_resource(item):
    water = resource["Water"]
    coffee = resource["Coffee"]
    milk  = resource["Milk"]
    #print(f"Resource: water: {water} coffee: {coffee} milk: {milk}")
    if menu[item]["Water"] < water and menu[item]["Coffee"] < coffee and menu[item]["Milk"] < milk:
        return True
    else:
        print("Out of stock. Sorry for the inconvenience")
        return False

def cash_machine(q,d,n,p,item):
    user_sum = ((q*0.25)+(d*0.10)+(n*0.05)+(p*0.01))
    item_cost = menu[item]["Cost"]
    if user_sum > item_cost:
        balance=user_sum-item_cost
        print(f"your balance amount: {round(balance)}")
        resource["Money"] = item_cost
        return True
    else:
        print(f"Insufficient money, Here's your change: {user_sum}")
        return False


def update_resource(item):
    if item == "espresso":
        resource["Water"] = resource["Water"] - menu[item]["Water"]
        resource["Coffee"] = resource["Coffee"] - menu[item]["Coffee"]
    else:
        resource["Water"] = resource["Water"] - menu[item]["Water"]
        resource["Milk"] = resource["Milk"] - menu[item]["Milk"]
        resource["Coffee"] = resource["Coffee"] - menu[item]["Coffee"]




while machine_power:
    user_choice = input('What would you like? (espresso/latte/cappuccino):').lower()

    if user_choice == "resource":
        print(resource)
        exit()

    stock_check = check_resource(user_choice)
    print(stock_check)

    if stock_check:

        print("Please insert the coins:")
        quarters = int(input("Please enter the quarters:"))
        dime = int(input("Please enter the dime:"))
        nickles = int(input("Please enter the nickles:"))
        pennies = int(input("Please enter the pennies:"))

        paid = cash_machine(q=quarters, d=dime, n=nickles, p=pennies, item=user_choice)

        if paid:

            if user_choice == "espresso":
                print("Making espresso....[estd time 1 minute]")
                update_resource(user_choice)
                sleep(10)
                print(f"{user_choice} is ready!")
            elif user_choice == "latte":
                print("Making latte....[estd time 1 minute]")
                update_resource(user_choice)
                sleep(12)
                print(f"{user_choice} is ready!")
            elif user_choice == "cappuccino":
                print("Making cappuccino....[estd time 1 minute]")
                update_resource(user_choice)
                sleep(14)
                print(f"{user_choice} is ready!")

    if user_choice == "off":
        machine_power = False
        print("Coffee machine turning OFF.")
    else:
        print("Coffee machine turning OFF.")
        machine_power = False