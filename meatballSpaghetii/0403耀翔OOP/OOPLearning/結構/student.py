class Student:
    """
    attribute: id, name, schoolName

    method: getId(self,), getName(self,), getSchoolName(self,), setSchoolName(self,),  setName(self, name)
    """

    #attribute
    id =""
    name =""
    schoolName ="Yuntech"
    
    #constructor
    def __init__(self, id, name ):
        self.id =id
        self.name =name

    #method
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getSchoolName(self):
        return self.schoolName
    def setSchoolName(self):
        self.schoolName = "Formosa"

    def setName(self, name):
        self.name =name