# class person(object):
#     tall = 180
#     hobbies = []
#     def __init__(self, name, age,weight):
#         self.name = name
#         self.age = age
#         self.weight = weight
#     def infoma(self):
#         print('%s is %s weights %s'%(self.name,self.age,self.weight))
# person.hobbies.extend(["football", "woman"])   
# print("person hobbies list: %s" %person.hobbies)    ## person hobbies list: ['football', 'woman']
# person.hobbies2 = ["reading", "jogging", "swimming"]  
# print("person hobbies2 list: %s" %person.hobbies2)  ## person hobbies2 list: ['reading', 'jogging', 'swimming']
# print(dir(person))
# ## ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', 
# # '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', 
# # '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', 
# # '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
# # 'hobbies', 'hobbies2', 'infoma', 'tall']


# #实例数据属性只能通过实例访问
# Bruce = person("Bruce", 25,60)    
# print ("%s is %d years old" %(Bruce.name, Bruce.age)   )
# # 在实例生成后，还可以动态添加实例数据属性，但是这些实例数据属性只属于该实例
# # 重新实例化的对象不包含实例数据属性
# Bruce.gender = "male"   
# print( "%s is %s" %(Bruce.name, Bruce.gender) )  
# # 可以通过类属性访问该实例
# print(dir(Bruce))
# # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
# # '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
# # '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
# # '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
# # 'age', 'gender', 'hobbies', 'infoma', 'name', 'tall', 'weight']
# Bruce.hobbies.append("C#")
# print(Bruce.hobbies)    ## ['C#']

##########################################
class object_example:
    def __init__(self) -> None:
        pass

class person(object_example):
    '''there is doc'''
    tall = 180
    hobbies = []
    def __init__(self, name, age,weight):
        self.name = name
        self.age = age
        self.weight = weight
    def infoma(self):
        print('%s is %s weights %s'%(self.name,self.age,self.weight))

print(person.__name__)      # person
print(person.__doc__)       # there is doc
print(person.__bases__)     # (<class '__main__.object_example'>,)
print(person.__dir__)       # <method '__dir__' of 'object' objects>
print(person.__module__)    # __main__
print(person.__class__)     # <class 'type'>
