from abc import ABC, abstractmethod
#透過interface 把重複的calArea實作 不一樣的就區隔開 不要混為一談
class CalArea:
    @abstractmethod
    def calArea(self):
        pass

class Rectangle_(CalArea) :
    w, h =0, 0
    def setW(self, w): 
        self.w =w
    def setH(self, h): 
        self.h =h

    #override
    def calArea(self):
        return self.w *self.h
    
class Square_(CalArea):
    side =0
    def setSide(self, s):
        self.side =s
    
    #override
    def calArea(self):
        return self.side *self.side