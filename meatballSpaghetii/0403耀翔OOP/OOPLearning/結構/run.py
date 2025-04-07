from student import Student

#make objects
keller = Student("B11123005", "Keller")
eason =Student("B11123038", "Eason")


#procedure call = message = (use mathod to call) 
print(keller.getId(), eason.getId())

keller.setSchoolName()
print(keller.getSchoolName(), eason.getSchoolName())

keller.setName("meatball spaghetii")
eason.setName("black man")

print(keller.getName(), ", ", eason.getName())