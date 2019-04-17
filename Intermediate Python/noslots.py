class MyClass(object):
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier
        
num = 1024*256
x = [MyClass(1,1) for i in range(num)]