from exampleClass import Student, StudentA, StudentB, StudentAI

keller =Student("B11123005", "Keller")
keller.setGrade("四資管二A")
print(keller.getGrade()) #getter
print(keller._grade) #_data hiding只是標記，直接調用也是可以

keller =StudentA("A11123005", "Keller")#執行的時候才知道他是一種studentA
keller.setGrade("四資管二A") #知道是studentA後 跑到這行才動態綁定孩子的setGrade
print(keller.getGrade()) 



from exampleClass2 import calArea
calculator =calArea()

print(calculator.calAreaCorrect(12, 3))
#print(calculator.calAreaNum(5))
print(calculator.calAreaCorrect(12))