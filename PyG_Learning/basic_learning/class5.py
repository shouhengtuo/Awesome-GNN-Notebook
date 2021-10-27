# class Parent(object):
#     '''parent class'''
#     numList = []
#     def numdiff(self, a, b):
#         return a-b

# class Child(Parent):
#     pass

# c = Child()    
# # 子类继承父类的属性   
# Child.numList.extend(range(10))
# print(Child.numList)                ## [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# print("77 - 2 =", c.numdiff(77, 2)) ## 77 - 2 = 75

# # built-in function issubclass() 
# print(issubclass(Child, Parent))    ## True
# print(issubclass(Child, object))    ## True

# # _ _bases_ _ 属性查看父类
# print('the bases are:',Child.__bases__)     ## the bases are: (<class '__main__.Parent'>,)

# # doc 属性不会被继承
# print(Parent.__doc__)   ## parent class
# print(Child.__doc__)    ## None

######################################################
# 定义父类：Parent
# class Parent(object):
#     def __init__(self, name):
#         self.name = name
#         print("create an instance of:", self.__class__.__name__)
#         print("name attribute is:", self.name)
# # 定义子类Child ，继承父类Parent       
# class Child(Parent):
#     pass
# # 子类实例化时，由于子类没有初始化，此时父类的初始化函数就会默认被调用
# # 且必须传入父类的参数name
# c = Child() 

######################################################
# class Parent(object):
#     def __init__(self, name):
#         self.name = name
#         print("create an instance of:", self.__class__.__name__)
#         print("name attribute is:", self.name)
# # 子类继承父类        
# class Child(Parent):
#     # 子类中没有显示调用父类的初始化函数
#     def __init__(self):
#         print("call __init__ from Child class")
# # c = Child("init Child") 
# # print()  
# # 将子类实例化  
# c = Child()
# print(c.name)

######################################################
# class Parent(object):
#     def __init__(self, name):
#         self.name = name
#         print("create an instance of:", self.__class__.__name__)
#         print("name attribute is:", self.name)

# class Child(Parent):
#     def __init__(self):
#         print("call __init__ from Child class")
#         super(Child,self).__init__("data from Child")   # 要将子类 Child 和 self 传递进去
# # c = Child("init Child") 
# # print() 
# d = Parent('tom')   
# c = Child()
# print(c.name)

######################################################
# class Parent(object):
#     Value = "Hi, Parent value"
#     def fun(self):
#         print("This is from Parent")
# # 定义子类，继承父类               
# class Child(Parent):
#     Value = "Hi, Child  value"
#     def ffun(self):
#         print("This is from Child")

# c = Child()    
# c.fun()             ## This is from Parent
# c.ffun()            ## This is from Child
# print(Child.Value)  ## Hi, Child  value

######################################################
# class Parent(object):
#     Value = "Hi, Parent value"
#     def fun(self):
#         print("This is from Parent")

# class Child(Parent):
#     Value = "Hi, Child  value"
#     def fun(self):
#         print("This is from Child")
#         Parent.fun(self)   # 调用父类Parent的fun函数方法

# c = Child() 
# # 实例化子类Child的fun函数时，首先会打印上条的语句，再次调用父类的fun函数方法
# c.fun()     ## This is from Child \n This is from Parent

######################################################
# E