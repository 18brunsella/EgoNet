class Circle:
    def __init__(self,circle_name,alters):
        self.__alters = alters
        self.__circle_name = circle_name

    def get_circle_name(self):
        return self.__circle_name

    def get_alters(self):
        return self.__alters

    def get_circle_size(self):
        return len(self.__alters)

    def add_alter(self,alter):
        self.__alters.append(alter)

    def __contains__(self,alter):
        for node in self.__alters:
            if node.get_id() == alter.get_id():
                return True
        else:
            return False
        
    def __eq__(self,other):
        return (self.__alters == other.__alters) and (self.__circle_name == other.__circle_name)
        
    def __str__(self):
        st = f"Circle Name: {self.__circle_name}"
        st+= f"Alters in circle: {self.__alters}"
        return st

    __repr__ = __str__
