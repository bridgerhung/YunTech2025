from abc import ABC, abstractmethod
"""
abstract class: bird
interface: flyable

eagle繼承bird, 實作fly, override sleep跟walk
penguin繼承bird, override sleep跟work
麻雀繼承bird, 實作fly, orverride walk

py因為支援多重繼承 方式彈性 是不是interface還是abstract class 其實沒有那麼重點
"""

#abstract method
class Bird:
    def sleep(self):
        print("sleeping")
        
    @abstractmethod
    def walk(self):
        pass
        
#interface
class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass

#繼承bird, 實作fly, override sleep跟walk
class Eagle(Bird, Flyable):
    def fly(self):
        print("eagle flying")
    def sleep(self):
        print("eagle sleeping")

    def walk(self):
        print("雙腳行走")

#只繼承bird, override sleep跟work
class Penguin(Bird):
    def sleep(self):
        print("penguin sleeping")

    def work(self):
        print("雙腳行走")

#繼承bird, 實作fly, orverride walk
class 麻雀(Bird, Flyable):
    def fly(self):
        print("麻雀flying")
    
    #因為bird有定義sleep 所以麻雀沒有override sleep的話 會動態綁定bird的sleep

    def walk(self):
        print("雙腳併攏跳躍行走")
