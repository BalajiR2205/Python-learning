import random
import turtle
from random import choice

import heroes

timmy = turtle.Turtle()
timmy.shape("arrow")

# print(heroes.gen())
#
# for num in range(0,4):
#     timmy.forward(100)
#     timmy.right(90)

# for _ in range(50):
#     timmy.forward(10)
#     timmy.color("white")
#     timmy.forward(10)
#     timmy.color("black")

#drawing shapes

# sides_of_shape = 3
colors = ['#FFFF00','#EE82EE','#00F5FF','#FF6347','#D8BFD8','#FFA54F','#63B8FF','#00FF7F','#836FFF','#FF0000']
#
# while sides_of_shape <= 10:
#     timmy.pencolor(choice(colors))
#     angle = round(360 / sides_of_shape)
#     #print(angle)
#     for _ in range(sides_of_shape):
#         timmy.forward(40)
#         timmy.left(angle)
#         timmy.forward(40)
#     sides_of_shape+=1

#RANDOM WALK!!!!!!

# movement = ["w","d","s","a"]
#
# distance = 0
#
turtle.speed('fastest')
# #turtle.shapesize(5, 5, 12)
# #turtle.turtlesize(5, 5, 12)
#
# while distance <= 100:
#     turtle.speed(10)
#     timmy.pensize(10)
#     timmy.pencolor(choice(colors))
#
#     side = choice(movement)
#     if side =="w":
#         timmy.forward(30)
#     elif side =="d":
#         timmy.right(90)
#         timmy.forward(30)
#     elif side =="s":
#         timmy.backward(50)
#     elif side =="a":
#         timmy.left(90)
#         timmy.forward(30)
#     distance+=1
turtle.colormode(255)

def random_color():
    r = random.randint(0,255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r,g,b)
    return color

def generate_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        timmy.color(random_color())
        timmy.circle(50)
        timmy.setheading(timmy.heading() + size_of_gap)

generate_spirograph(5)

screen = turtle.Screen()
screen.exitonclick()