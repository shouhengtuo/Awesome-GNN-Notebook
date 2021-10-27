# from example_example import *
# #调用不带下划线函数
# call_for()
# #调用不带下划线函数会报错
# _call_for()


# class person(object):
#     tall = 180
#     hobbies = []
#     def __init__(self, name, age,weight):
#         self.name = name
#         self.age = age
#         self.weight = weight
#         self.__Id = 430
#     @staticmethod
#     def infoma():
#         print(person.tall)
#         print(person.hobbies)
# person.infoma()
# Bruce = person("Bruce", 25,180)
# print(Bruce.__Id)
# Bruce.infoma() 

class A(object):
    def __init__(self):
        self.__private()
        self.public()
    
    def __private(self):
        print('A.__private()')
    
    def public(self):
        print('A.public()')

class B(A):
    def __private(self):
        print('B.__private()')
    
    def public(self):
        print('B.public()')
b = B()
b.__private()
b._A__private()


