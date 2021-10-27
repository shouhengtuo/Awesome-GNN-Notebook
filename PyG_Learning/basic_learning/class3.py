# class person(object):
#     tall = 180
#     hobbies = []
#     def __init__(self, name, age,weight):
#         self.name = name
#         self.age = age
#         self.weight = weight
#     def infoma(self):
#         print('%s is %s weights %s'%(self.name,self.age,self.weight))


# Bruce = person("Bruce", 25,180)
# Bruce.infoma()  # Bruce is 25 weights 180

#########################################################
# class person(object):

#     tall = 180
#     hobbies = []
#     def __init__(self, name, age,weight):
#         self.name = name
#         self.age = age
#         self.weight = weight
#     @classmethod     #类的装饰器
#     def infoma(cls):   #cls表示类本身，使用类参数cls
#         print(cls.__name__)
#         print(dir(cls))
# # 1. 直接调用类的装饰器函数，通过cls可以访问类的相关属性
# person.infoma()
# # 2. 通过两步骤来实现，第一步实例化person，第二步调用装饰器  
# # Bruce = person("Bruce", 25,180)   
# # Bruce.infoma() 

##########################################################
class person(object):

    tall = 180
    hobbies = []
    def __init__(self, name, age,weight):
        self.name = name
        self.age = age
        self.weight = weight
    @staticmethod    #静态方法装饰器
    def infoma():     #没有参数限制，既不要实例参数，也不用类参数
        print(person.tall)
        print(person.hobbies)
# 1. 通过类名访问
#person.infoma()
# 2. 通过实例访问  
Bruce = person("Bruce", 25,180)   
Bruce.infoma() 