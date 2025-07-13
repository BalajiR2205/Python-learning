from turtle import Turtle
import random
#from snake import Snake

class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()


    def refresh(self):
        x_cor = random.randint(a=-280,b=280)
        y_cor = random.randint(a=-280,b=280)
        self.goto(x_cor,y_cor)


