import turtle
import prettytable

#creating a object

# timmy = turtle.Turtle()
# print(timmy)
# timmy.shape("turtle")
# timmy.shapesize(5, 5, 5)
# timmy.color("red","green")
# timmy.forward(100)
# for num in range(0,10):
#     timmy.forward(100)
#     timmy.right(100)
#
#
# my_screen = turtle.Screen()
#
# print(my_screen.canvheight)
#
# my_screen.exitonclick()

table = prettytable.PrettyTable()
table.add_column("pokemon name",["pikachu", "squirtle","CHalamander"])
table.add_column("Type",["Electric", "Water","Fire"])

table.align="r"

print(table)