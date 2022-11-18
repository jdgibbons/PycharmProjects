import math

class Line:

    def __init__(self, coor1, coor2):
        self.coor1 = coor1
        self.coor2 = coor2

    def distance(self):
        x_change = self.coor2[0] - self.coor1[0]
        y_change = self.coor2[1] - self.coor1[1]

        x_squared = x_change ** 2
        y_squared = y_change ** 2

        xy_sum = x_squared + y_squared

        xy_root = xy_sum ** .5

        print(f"xy_root = {xy_root}")
        print(f"sqrt(xy_sum) = {math.sqrt(xy_sum)}")

        return (((self.coor1[0] - self.coor2[0]) ** 2) + ((self.coor2[1] - self.coor1[1]) ** 2)) ** .5

    def slope(self):
        return (self.coor2[1] - self.coor1[1]) / (self.coor2[0] - self.coor1[0])


coordinate1 = (3, 2)
coordinate2 = (8, 10)

li = Line(coordinate1, coordinate2)
print(f"Distance = {li.distance()}")
print(f"Slope = {li.slope()}")