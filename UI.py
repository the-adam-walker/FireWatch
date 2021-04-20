##############################
#  UI for FireWatch Project  #
##############################

from tabulate import tabulate
import turtle

TURTLE_SIZE=20

def triangle1 (heading):
    tri1=turtle.Turtle(visible = False)
    tri1.penup()
    tri1.goto(30,0)
    tri1.pendown()
    tri1.setheading(heading)
    tri1.showturtle()

def triangle2 (heading):
    tri2=turtle.Turtle(visible = False)
    tri2.penup()
    tri2.goto(30,25)
    tri2.pendown()
    tri2.setheading(heading)
    tri2.showturtle()

def triangle3 (heading):
    tri3=turtle.Turtle(visible = False)
    tri3.penup()
    tri3.goto(30,50)
    tri3.pendown()
    tri3.setheading(heading)
    tri3.showturtle()

#passed in data for name(?), distance, and heading
#placeholder examples
moduleNames = ('NodeA', 'NodeB', 'NodeC')
distance = ('13m', '7m', '12m')
direction = (triangle1(120), triangle2(30), triangle3(250))


table = [[moduleNames[0], distance[0], direction[0]],
         [moduleNames[1], distance[1], direction[1]],
         [moduleNames[2], distance[2], direction[2]]]

headers = ["Name", "Distance", "Direction"]

print(tabulate(table, headers))
