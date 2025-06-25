student_scores = [150, 142, 185, 120, 171, 184, 149, 24, 59, 68, 199, 78, 65, 89, 86, 55, 91, 64, 89]

print(max(student_scores))

max_score = 0
for score in student_scores:
    if score > max_score:
        max_score = score

print(max_score)

sum=0

for num in range(0,101):
    sum+=num
print(sum)

import random

#Random password generator

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

pwd_letters = []
pwd_symbols = []
pwd_numbers = []

for char in range(1, nr_letters + 1):
    pwd_letters += random.choice(letters)

for char in range(1, nr_symbols + 1):
    pwd_symbols += random.choice(symbols)

for char in range(1, nr_numbers + 1):
    pwd_numbers += random.choice(numbers)

#print(pwd_letters)
#print(pwd_symbols)
#print(pwd_numbers)

total=pwd_letters+pwd_numbers+pwd_symbols

print(total)

random.shuffle(total)

print(total)

final_pwd=''.join(total)
print(final_pwd)