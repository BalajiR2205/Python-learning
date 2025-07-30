#import time
#from turtle import Turtle
from turtle import Screen

MOVE_FORWARD = 20

from paddle import Paddle

screen = Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("Pong Game")
screen.tracer(0)

r_paddle = Paddle((380, 0))
l_paddle = Paddle((-390, 0))

# pad = Turtle("square")
# pad.color("white")
# pad.shapesize(5, 1)
# pad.penup()
# pad.goto(380, 0)


screen.listen()
screen.onkey(r_paddle.r_up,"Up")   
screen.onkey(r_paddle.r_down,"Down")
screen.onkey(l_paddle.l_up,"w")
screen.onkey(l_paddle.l_down,"s")

game_is_on = True

while game_is_on:
    screen.update()


#pad.create_pads()
















screen.exitonclick()