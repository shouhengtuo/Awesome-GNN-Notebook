# https://www.cnblogs.com/kongk/p/8644745.html
# #-*- coding：utf-8 -*-<br>
# class A(object):
#     def __init__(self,xing,gender):         #！#1
#         self.namea="aaa"                    #！#2
#         self.xing = xing                    #！#3
#         self.gender = gender                #！#4
         
#     def funca(self):
#         print("function a : %s"%self.namea)
  
# class B(A):
#     def __init__(self,xing,age):            #！#5
#         super(B,self).__init__(xing,age)    #！#6（age处应为gender）
#         self.nameb="bbb"                    #！#7
#         ##self.namea="ccc"                  #！#8
#         ##self.xing = xing.upper()          #！#9
#         self.age = age                      #！#10
         
#     def funcb(self):
#         print("function b : %s"%self.nameb)
  
# b=B("lin",22)                               #！#11
# print(b.nameb)
# print(b.namea)
# print(b.xing)                                #！#12
# print(b.age)                                 #！#13
# print(b.gender)
# b.funcb()
# b.funca()
class A(object):
    def __init__(self,xing,gender):
        self.namea="aaa"
        self.xing = xing
        self.gender = gender
         
    def funca(self):
        print("function a : %s"%self.namea)
  
class B(A):
    def __init__(self,xing,gender,age):
        super(B,self).__init__(xing,gender)
        self.nameb="bbb"
        ##self.namea="ccc"
        self.xing = xing.upper()       
        self.age = age + 1
        #self.gender = gender.upper()
         
    def funcb(self):
        print("function b : %s"%self.nameb)
  
b=B("lin","nan0",22)
print(b.nameb)
print(b.namea)
print(b.xing)
print(b.age)
b.funcb()
b.funca()
print(b.gender)   #####