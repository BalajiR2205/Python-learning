import turtle

STARTING_POSITION = [(380, 0), (-385, 0)]

class Paddle:
    # pad = turtle.Turtle("rectangle")
    def __init__(self, position):
        print(f"Object created for: {position}")
        self.pads = []
        self.create_pads(position)
        # self.paddle_one=self.pads[0]
        # self.paddle_two=self.pads[1]

    def create_pads(self, position):
        #for position in STARTING_POSITION:
        pad = turtle.Turtle("square")
        pad.color("white")
        pad.shapesize(5, 1)
        pad.penup()
        pad.goto(position)
        self.pads.append(pad)
        #print(self.pads)
        #

    def r_up(self):
        #for pads in self.pads:
        print(self.pads)
        new_y = self.pads[0].ycor() + 20
        self.pads[0].goto(self.pads[0].xcor(), new_y)

    def r_down(self):
        #for pads in self.pads:
        new_y = self.pads[0].ycor() - 20
        self.pads[0].goto(self.pads[0].xcor(), new_y)

    def l_up(self):
        #for pads in self.pads:
        new_y = self.pads[0].ycor() + 20
        self.pads[0].goto(self.pads[0].xcor(), new_y)

    def l_down(self):
        print(self.pads)
        #for pads in self.pads:
        new_y = self.pads[0].ycor() - 20
        self.pads[0].goto(self.pads[0].xcor(), new_y)
