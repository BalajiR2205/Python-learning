import random

print("Welcome to black jack 21:")

user_choice = input(print("Press 'y' to start the game or 'n' to end the game"))

cards = [11,2,3,4,5,6,7,8,9,10,10,10,10]

computer_deck = []
user_deck = []

def print_deck():
    print(f"Computer's deck:{computer_deck}")
    print(f"User's deck:{user_deck}")

def is_blackjack(deck):
    if sum(deck) == 21:
        return True
    else:
        return False


def push():
    random_index = random.randint(0,12)
    card=cards[random_index]
    return card

def win_check():
    if sum(computer_deck) < sum(user_deck) < 21:
        print("You win! congratulations")
        print_deck()
    else:
        print("Computer won. Better luck next time!")
        print_deck()

if user_choice == "y":
    for turn in range(0,2):
        computer_deck.append(push())
        user_deck.append(push())
    if is_blackjack(computer_deck):
        print("Computer got blackjack!")
    elif is_blackjack(user_deck):
        print("User got blackjack!")
    else:
        if sum(computer_deck) < 16:
            computer_deck.append(push())
        print(computer_deck[0])
        print(user_deck)
        next_move=input(print("Do you want to push or hold? (P/H)")).lower()
        if next_move == "p":
            user_deck.append(push())
            win_check()
        elif next_move == "h":
            win_check()

elif user_choice == "n":
    print("Thanks for checking out!")

else:
    print("Enter a valid input")