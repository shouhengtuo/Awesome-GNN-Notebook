# # 面向过程编程
# 多函数程序中，许多重要数据被放置在全局数据区，可以被所有的函数访问
# 每个函数都可以具有他们自己的局部数据

# # 面向对象编程
# 将函数和变量进一步封装成类，类是程序的基本元素，将数据和操作紧密连接。保护数据不会被外界函数意外改变

# # 专业术语
# 1. 类(Class): 用来描述具有相同属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。其中的对象被称作类的实例。
# 2. 实例：也称对象。通过类定义的初始化方法，赋予具体的值，成为一个“有血有肉的实体”。
# 3. 实例化：创建类的实例的过程或操作。
# 4. 实例变量：定义在实例中的变量，只作用于当前实例。
# 5. 类变量：类变量是所有实例公有的变量。类变量定义在类中，但在方法体之外。
# 6. 数据成员：类变量、实例变量、方法、类方法、静态方法和属性等的统称。
# 7. 方法：类中定义的函数。
# 8. 静态方法：不需要实例化就可以由类执行的方法
# 9. 类方法：类方法是将类本身作为对象进行操作的方法。
# 10. 方法重写：如果从父类继承的方法不能满足子类的需求，可以对父类的方法进行改写，这个过程也称override。
# 11. 封装：将内部实现包裹起来，对外透明，提供api接口进行调用的机制
# 12. 继承：即一个派生类（derived class）继承父类（base class）的变量和方法。
# 13. 多态：根据对象类型的不同以不同的方式进行处理。

# # 静态方法
class ff:
    @staticmethod
    def runx():
        print("static method")
ff.runx()

# # 魔法方法
# 1. __init__ :      构造函数，在生成对象时调用
# 2. __del__ :       析构函数，释放对象时使用
# 3. __repr__ :      打印，转换
# 4. __setitem__ :   按照索引赋值
# 5. __getitem__:    按照索引获取值
# 6. __len__:        获得长度
# 7. __cmp__:        比较运算
# 8. __call__:       调用
# 9. __add__:        加运算
# 10. __sub__:        减运算
# 11. __mul__:        乘运算
# 12. __div__:        除运算
# 13. __mod__:        求余运算
# 14. __pow__:        幂