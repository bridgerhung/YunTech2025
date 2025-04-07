
class Rectangle:
    side1, side2 =0, 0

    def __init__(self):
        pass

    def setSide1(self, side):
        self.side1 =side
    
    def setSide2(self, side):
        self.side2 =side

    def calArea(self):
        return self.side1 *self.side2
    

class Square(Rectangle):
    def setSide1(self, side):
        self.side1 =side
        self.side2 =side
    #override
    def setSide2(self, side):
        self.side1 =side
        self.side2 =side