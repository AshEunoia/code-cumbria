# 2025-10-14-12-54-09

'''
Using what you've learned about Classes and Inheritance, write a Python program to model
some calculations of shapes:
- area
- perimeter

You may wish to draw a set of class
diagrams, but this is not essential.

Specifically, implement a base class called Shape, and child classes for:
- Shape
  - Circle
  - Rectangle
  - Triangle

Provide methods to initialise each class, and methods to return the area and perimeter of
each class.

Write some test code for each shape, printing out the properties of each shape and the
calculated area and perimeter.

Note: You will need to import the math library to access useful values like Pi
Save your finished code as OOPAssignment.py and commit it to your GitHub repository.

Submit a link to the file in your repository on Trainer Central under the OOP Assignment
section.
'''

import numpy

class Shape():
  def __init__(self):
    pass

  def area(self):
    pass

  def perimeter(self):
    pass

class Circle(Shape):
  def __init__(self, radius: float):
    self.radius = radius

  # pi * r**2
  def area(self):
    return numpy.pi * self.radius**2

  # 2 * pi * r
  def perimeter(self):
    return 2 * numpy.pi * self.radius

class Rectangle(Shape):
  # Only 2 sides need to be given.
  def __init__(self, side_0: float, side_1: float):
    self.side_0 = side_0
    self.side_1 = side_1

  # a + b
  def area(self):
    return self.side_0 * self.side_1

  # (a + b) * 2
  def perimeter(self):
    return (self.side_0 + self.side_1) * 2

class Triangle(Shape):
  def __init__(self, side_0: float, side_1: float, side_2: float):
    assert not (
      side_0 > side_1 + side_2 or 
      side_1 > side_0 + side_2 or 
      side_2 > side_0 + side_1), "No side of a triangle can be greater than the sum of the other two sides."

    self.side_0 = side_0
    self.side_1 = side_1
    self.side_2 = side_2

  # Based on the numerically stable version of Heron's formula: https://en.wikipedia.org/wiki/Heron%27s_formula?useskin=vector.
  # sqrt((a + (b + c)) * (c - (a - b)) * (c + (a - b)) * (a + (b - c)))/4
  def area(self):
    # Sort descending.
    # I'm not sure this really does anything, but the wiki seems to consider it important!
    sides = numpy.flip(numpy.sort([self.side_0, self.side_1, self.side_2]))

    return(
      numpy.sqrt(
        (sides[0] + (sides[1] + sides[2])) * 
        (sides[2] - (sides[0] - sides[1])) * 
        (sides[2] + (sides[0] - sides[1])) * 
        (sides[0] + (sides[1] - sides[2]))
      )/4)

  # a + b + c
  def perimeter(self):
    return self.side_0 + self.side_1 + self.side_2

def test_print(shape):
  print(
    "Shape: " + str(type(shape).__name__) + 
    "\n  Properties: " + str(vars(shape)) + 
    "\n  Area______: " + str(shape.area()) + 
    "\n  Perimeter_: " + str(shape.perimeter()))

test_print(Circle(3))
test_print(Rectangle(5, 2))
test_print(Triangle(5, 2, 6))
