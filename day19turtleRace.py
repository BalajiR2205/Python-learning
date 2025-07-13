import random
import turtle
from turtle import Turtle, Screen

screen=Screen()

is_race_on = False

# def create_turtle(turtle_color,y_pos):
#     t_color = turtle_color
#     turtle_color = Turtle(shape="turtle")
#     turtle_color.fillcolor(t_color)
#     turtle_color.penup()
#     turtle_color.goto(-240, y_pos)



screen.setup(500, 400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win race? Enter a color: ")
# tim = Turtle(shape="turtle")
print(user_bet)

colors = ["green","blue","orange","yellow","brown","purple"]
y_pos = [-70,-40,-10,20,50,80]

all_turtles = []

for _ in range(0,6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.color(colors[_])
    new_turtle.goto(x=-230, y=y_pos[_])
    all_turtles.append(new_turtle)

if user_bet:
    is_race_on=True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 225:
            #print(turtle.fillcolor())
            winning_color = turtle.pencolor()
            is_race_on = False
            if winning_color == user_bet:
                print(f"you win! {turtle.fillcolor()} turtle won")
            else:
                print(f"you lose :( {turtle.fillcolor()} won")

        random_distance  = random.randint(0,10)
        turtle.forward(random_distance)









screen.exitonclick()
