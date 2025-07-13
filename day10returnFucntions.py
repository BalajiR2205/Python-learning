def function1(text):
    return text + text

def function2(text):
    titled = text.title()
    return titled

output = function2(function1("Hello"))

print(output)