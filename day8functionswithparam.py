# def greet():
#     print("hello")
#     print("hola")
#     print("bye")
#
# greet()
#
# def great_with(name, location):
#     print(f"Hello {name}, What's the weather in {location}?")
#
# great_with("jack sparrow","Treasure island")
#
# great_with(location="Treasure island", name="Jack sparrow") #positional arguments

#Ceaser Cypher:

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower() #x:22 y:13 z: 11
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))

alphabet_length = len(alphabet)


# TODO-1: Create a function called 'encrypt()' that takes 'original_text' and 'shift_amount' as 2 inputs.

# TODO-2: Inside the 'encrypt()' function, shift each letter of the 'original_text' forwards in the alphabet
#  by the shift amount and print the encrypted text.

# TODO-4: What happens if you try to shift z forwards by 9? Can you fix the code?

# TODO-3: Call the 'encrypt()' function and pass in the user inputs. You should be able to test the code and encrypt a
#  message.

power_on=True

def encode(message, shiftnumber):
    encrypted_word = ""
    for char in message:
        print(f"loop for: {char}")
        original_index = alphabet.index(char)
        print(f"Original num: {original_index} shift number: {shiftnumber}")
        if original_index+shiftnumber > 25:
            encrypted_char = alphabet[(original_index+shiftnumber)-alphabet_length]
            print(f"decrypted char in if: {encrypted_char}")
        else:
            encrypted_char = alphabet[original_index+shiftnumber]
            print(f"decrypted char in else: {encrypted_char}")
        encrypted_word += encrypted_char
    print(encrypted_word)
        #power_on = False

def decode(message, shiftnumber):
    decrypted_word = ""
    for char in message:
        print(f"loop for: {char}")
        original_index = alphabet.index(char)
        print(f"Original num: {original_index} shift number: {shiftnumber}")
        decrypted_char = alphabet[original_index-shiftnumber]
        print(f"decrypted char: {decrypted_char}")
        decrypted_word += decrypted_char
    print(decrypted_word)
        #power_on = False



if direction == "encode":
    encode(text, shift)
elif direction == "decode":
    decode(text, shift)


