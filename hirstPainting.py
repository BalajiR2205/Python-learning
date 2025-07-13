import colorgram

import turtle as turtle_module

import random

# colors = colorgram.extract('img.png', 48)
#
# first_color = colors[0]
#
# print(first_color.rgb)
#
# print(first_color.hsl)
#
# rgb_color = []
#
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     color_tuple = (r,g,b)
#     rgb_color.append(color_tuple)

timmy = turtle_module.Turtle()

turtle_module.colormode(255)


color_list = [(167, 20, 41), (19, 106, 155), (236, 222, 227), (191, 165, 116), (167, 99, 52), (219, 230, 239), (97, 184, 139), (162, 51, 92), (221, 204, 113), (222, 67, 45), (201, 116, 157), (155, 175, 35), (26, 55, 120), (38, 171, 192), (75, 32, 39), (235, 202, 4), (131, 182, 199), (44, 47, 69), (53, 37, 29), (32, 173, 142), (117, 113, 176), (147, 34, 23), (198, 82, 108), (228, 169, 183), (161, 209, 190), (231, 174, 164), (153, 210, 218), (31, 135, 123), (182, 186, 212), (5, 106, 116), (10, 112, 109)]

#print(timmy.position())

timmy.hideturtle()

x_start = -250
y_start = -250

# print(20 % 10)
def set_to_position(x,y):
    timmy.penup()
    timmy.goto(x,y)

set_to_position(x_start,y_start)

for _ in range(100):
    if _ % 10 == 0:
        set_to_position(x_start, y_start)
        y_start += 50
    else:
        #print(timmy.position())
        timmy.dot(20, random.choice(color_list))
        timmy.penup()
        timmy.forward(50)


screen = turtle_module.Screen()
screen.exitonclick()
