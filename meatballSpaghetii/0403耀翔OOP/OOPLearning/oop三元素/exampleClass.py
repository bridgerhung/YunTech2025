#封裝 =class要有attributes +method 給他包
class Student:

    """
    用__表示private ==只有student才可以動，外面不要動
    _表示protected ==只有兒女才能用
    py沒有強制data_hiding 所以直接在外面跑student.name("sth.")也可以跑得動

    attr: _id, _name, _grade, schoolName

    method: getId(self), getName(self), getGrade(self), setId(self, newId), setName(self, newName), setGrade(self, newGrade):
    """
    #data hiding
    _id, _name, _grade ="", "", ""
    schoolName ="Formosa"

    def __init__(self, id, name) :
        self._id =id;  
        self._name =name;  
        

    def getId(self):
        return self._id
    def getName(self):
        return self._name
    def getGrade(self):
        return self._grade


    def setId(self, newId):
        self._id =newId
    def setName(self, newName):
        self._name =newName
    def setGrade(self, newGrade):
        self._grade ="資管系" + newGrade
    

#繼承
class StudentA(Student):
    #override 多型
    def setGrade(self, newGrade):
        self._grade ="資管二技: " + newGrade

class StudentB(Student):
    #override
    def setGrade(self, newGrade):
        self._grade ="資管四技: " + newGrade

class StudentAI(Student):
    #override
    def setGrade(self, newGrade):
        self._grade ="資管技優: " + newGrade




