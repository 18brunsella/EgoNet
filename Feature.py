class Feature():
    def __init__(self, feature_id, feature, feature_value):
        self.__feature_id = feature_id
        self.__feature_value = feature_value
        self.__feature = feature

    def get_feature_value(self):
        return self.__feature_value

    def get_feature_id(self):
        return self.__feature_id

    def get_feature_name(self):
        return self.__feature

    def __hash__(self):
        return hash(self.__feature+self.__feature_id)

    def __eq__(self, feature):
        """
        This functions checks if two Feature objects are equal ie
        if both are Feature objects, and
        if both have same feature name, and
        if both have same feature value,
        if both have same feature id
        """
        if (
            isinstance(feature, Feature)
            and self.__feature == feature.get_feature_name()
            and self.__feature_value == feature.get_feature_value()
            and self.__feature_id == feature.get_feature_id()
        ):
            return True
        else:
            return False

    def __str__(self):
        st = f"Feature id: {self.get_feature_id()}\n"
        st += f"Feature name: {self.get_feature_name()}\n"
        st += f"Feature value: {self.get_feature_value()}\n"
        return st

    __repr__=__str__
