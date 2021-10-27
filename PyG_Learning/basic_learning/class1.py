# #构建person的类
# class person():
#     name = ''           #首先定义一下变量
#     age = 0
#     __weight = 0
#     def __init__(self,name,age,weight):    #初始化变量
#         self.name = name    #重新给类的name变量赋值，并可以全局调用
#         self.age = age
#         self.__weight = weight
#     def infoma(self):     
#         print('%s is %s weights %s'%(self.name,self.age,self.__weight))
# person = person('bruce',25,60)      #将变量赋值给person类实例化
# print(person)
# # print(person.__weight)      # AttributeError: 'person' object has no attribute '__weight'
# infoma = person.infoma()    # 调用person类的infoma函数方法

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 00:31:07 2018
类的定义构建
@author: BruceWong
"""

class person():
    def __init__(self,name,age,weight):
        self.name = name
        self.age = age
        self.__weight = weight
    def __cmp__(self):
        pow_age = self.age.__pow__(2)
        print(pow_age)
    def __len__(self):
        name_del = self.name.__len__()
        print(name_del)
    def __add__(self):
        adds = self.age.__add__(self.__weight)
        print(adds)

    def infoma(self):
        '''def doc example'''
        print('%s is %s weights %s'%(self.name,self.age,self.__weight))
print(person.__class__)
print(person.__repr__)



person = person('bruce',25,60)
print(person)
infoma = person.infoma()
cmp = person.__cmp__()
lens = person.__len__()
adds = person.__add__()
print('doc is %s'%person.infoma.__doc__)
print('dir is %s'%person.__dir__)
print('delatter is %s'%person.__delattr__)
print('gt is %s'%person.__gt__)
print('hash is %s'%person.__hash__)
print('init is %s'%person.__init__)
print('new is %s'%person.__new__)

'''
output：
<class 'type'>
<slot wrapper '__repr__' of 'object' objects>
<__main__.person object at 0x0000020744E69668>
bruce is 25 weights 60
625
5
85
doc is None
dir is <built-in method __dir__ of person object at 0x0000020744E69668>
delatter is <method-wrapper '__delattr__' of person object at 0x0000020744E69668>
gt is <method-wrapper '__gt__' of person object at 0x0000020744E69668>
hash is <method-wrapper '__hash__' of person object at 0x0000020744E69668>
init is <bound method person.__init__ of <__main__.person object at 0x0000020744E69668>>
new is <built-in method __new__ of type object at 0x00000000617BDFD0>
'''
