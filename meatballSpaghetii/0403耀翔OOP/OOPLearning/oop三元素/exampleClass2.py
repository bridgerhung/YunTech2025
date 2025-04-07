class calArea:
    """
    py沒有正統的overload 所以calAreaNum會壞掉
    儘量少用overload 在py上意義不大
    """
    def calAreaNum(self, side1):
        return side1 *side1

    def calAreaNum(self, side1, side2):
        return side1 *side2
    
    def calAreaCorrect(self, side1, side2 =False):
        return side1 *side2 if side2 else side1 *side1
