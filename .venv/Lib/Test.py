moshe=lambda x: x*x
print(moshe(9))
sum_lambada= lambda x,y: x+y
print(sum_lambada(10,8))
import requests
url="https://api.example.com/data"
#response=requests.get(url)
#response_data=response.json()
class Person:
    name=" "
    age=0
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def greet(self):
        print(f"Your name is {self.name} and your age is {self.age}")
person1=Person("Moshe",9)
person1.greet()
#data=list(map(lambda x:x*2),response_data)