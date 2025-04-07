from correctArea import Rectangle_, Square_
from incorrectArea import Rectangle, Square

"""
兒子做的事可以比爸爸優秀，但是要做的跟爸爸一樣
"""

square =Square()
square.setSide1(3)
square.setSide2(6)
print(square.calArea())

square =Rectangle()
square.setSide1(3)
square.setSide2(6)
print(square.calArea())


square =Square_()
square.setSide(3)
square.setSide(6)
print(square.calArea())

#透過interface 把重複的calArea實作 不重複的就區隔開 不要混為一談
#square =Rectangle_()
#square.setSide1(3)
#square.setSide2(6)
rectangle =Rectangle_()
rectangle.setH(3)
rectangle.setW(6)

print(rectangle.calArea())