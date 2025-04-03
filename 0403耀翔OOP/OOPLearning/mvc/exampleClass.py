"""
模型控制資料的處理
view跟模型要資料去show
controller控制view跟模型
"""
class  Teacher:
    age, gratuated, address, car =0, "", "", ""
    
    def __init__(self, age, gratuated, address, car):
        self.age =age
        self.gratuated =gratuated
        self.address =address
        self.car =car

    def getAge(self): return self.age
    def getGratuated(self): return self.gratuated
    def getAddress(self): return self.address
    def getCar(self): return self.car
    def getAll(self): return f"{self.age} {self.gratuated} {self.address} {self.car}"

    def setAge(self, age):
        self.age =age
    def setGratuated(self, gratuated):
        self.gratuated =gratuated
    def setAddress(self, address):
        self.address =address
    def setCar(self, car):
        self.car =car

class TeacherView:
    def show(self, getInfo):
        print(f"infomation: {getInfo}")

class TeacherController:
    def __init__(self, age, gratuated, address, car):
        self.model =Teacher(age, gratuated, address, car)
        self.view =TeacherView()
    def showTeacher(self):
        self.view.show(self.model.getAll())
    def editTeacher(self, value, item ="age"):
        if item =="age":
            self.model.setAge(value)
        elif item =="gratuated":
            self.model.setGratuated(value)
        elif item =="address":
            self.model.setAddress(value)
        elif item =="car":
            self.model.setAddresss(value)
        else:
            print("WTF")