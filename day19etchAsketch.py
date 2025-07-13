from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()

#tim.shape("turtle")

def move_forward():
    tim.forward(10)
def move_backward():
    tim.backward(10)
def rotate_right():
    new_heading = tim.heading() - 10
    tim.setheading(new_heading)
def rotate_left():
    new_heading = tim.heading() + 10
    tim.setheading(new_heading)
def clear_screen():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()

# screen.listen()
# screen.onkey(fun=move_forward, key="space")

# while
screen.listen()
screen.onkey(fun=move_forward, key="w")
screen.onkey(fun=move_backward, key="s")
screen.onkey(fun=rotate_right, key="a")
screen.onkey(fun=rotate_left, key="d")
screen.onkey(fun=clear_screen, key="c")

screen.exitonclick()