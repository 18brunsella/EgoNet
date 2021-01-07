class Node:
    def __init__(self,id,number_of_features):
        self.__id = id
        self.__features = [None for i in range(number_of_features)]

    def __hash__(self):
        """
        This functions computes the hash of the Node object
        so that they can be used as keys in a dictionary and be used with operators such as "in"
        Do not change this!
        """
        return hash(self.__id)

    def get_id(self):
        return self.__id

    def get_features(self):
        return self.__features

    def get_feature_value(self,feature_pos):
        return self.__features[feature_pos].get_feature_value()

    def get_feature_name(self,feature_pos):
        return (self.__features[feature_pos].get_feature_name())

    def get_feature_id(self,feature_pos):
        return (self.__features[feature_pos].get_feature_id())

    def add_feature(self,feature_pos,feature):
        self.__features[feature_pos] = feature

    def __eq__(self,other):
        return (self.__id == other.__id) and (self.__features == other.__features)	

    def __str__(self):
        """
        String representation of the Node object.
        Do not change this!
        """
        st = f"Node id: {self.__id}\n"
        st += f"Features: {self.__features}\n"
        return st

    __repr__=__str__
