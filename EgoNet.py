import Circle

class EgoNet:
    def __init__(self,ego,ego_net_features):
        self.__ego = ego #Represents the Ego node for the EgoNet. type - Node object
        self.__social_network = {} # Represents the social network graph. type - dict where key = Node object 			        and value = list of Node objects key is connected to
        self.__social_network[ego] = set() # Represents the social network graph. type - dict where key = Node object 			        and value = list of Node objects key is connected to
        self.__alter_node_count = 0 # Represents the total number of alter nodes connected to our Ego
        self.__circles = {} #Represents the circles formed in our EgoNet. type - dict where key = circle name		      and value = set of Node objects in the circle
        self.__ego_net_features = ego_net_features # Represents the features for our Ego Net. type - dict where key = feature			           position in feature file (type - int) and value = tuple of feature name and			          feature id. This does not contain Feature objects but just strings. 


    def get_alter_node(self,node_id):
        for key in self.__social_network.keys(): 
            if key.get_id() == node_id: 
                node = key
                return node 
        return None
        
    def get_ego(self):
        return self.__ego
    
    def get_circle_names(self):
        circle_names = []
        for key in self.__circles.keys():
            if key not in circle_names:
                circle_names.append(key)
            
        return circle_names

    def get_circle(self, circle_name):
        return self.__circles[circle_name]
    
    def get_alters(self):
        alter_set = ()
        ego = self.__ego 
        ego_net = self.__social_network
        for key in ego_net:
            if key == ego:
                alter_set = ego_net[key]
                return alter_set
            
    def get_alter_node_count(self):
        return self.__alter_node_count
        

    def get_ego_net_features(self):
        return self.__ego_net_features

    def get_ego_net_feature(self, feature):
        for key in self.__ego_net_features.items():
            if int(key[0]) == int(feature): 
                features = key[1]
                return features
            
    
    def get_feature_pos(self, feature_name, feature_id):
        for pos,tup in self.__ego_net_features.items():
            if tup == (feature_name, feature_id): 
                return pos 
        
        return None 
    
    def get_alter_connections(self, alter):
        return self.__social_network[alter]
    
    def add_circle(self, circle_name, alters):
        
        self.__circles[circle_name] = Circle.Circle(circle_name, alters)
    
        return self.__circles
        
    def add_connection_between_alters(self,alter1,alter2):
        
        if alter2 not in self.__social_network[alter1]:
            self.__social_network[alter1].add(alter2)
        
        if alter1 not in self.__social_network[alter2]:
            self.__social_network[alter2].add(alter1)
    

    def add_alter_node(self, alter):
        
        if alter not in self.__social_network[self.__ego]:
                self.__social_network[self.__ego].add(alter)
                self.__alter_node_count += 1 
        else: 
                self.__social_network[self.__ego] = 0
        
        self.__social_network[alter] = set()
        
        if self.__ego not in self.__social_network[alter]:
                self.__social_network[alter].add(self.__ego)
        else: 
                self.__social_network[alter] = 0
        
        
    

    def __eq__(self,other):
        '''True if all attributes are equal.'''
        return (self.__ego == other.__ego)\
            and (self.__social_network == other.__social_network) \
            and (self.__alter_node_count == other.__alter_node_count) \
            and (self.__circles == other.__circles) \
            and (self.__ego_net_features == other.__ego_net_features)
            
    def __str__(self):
        '''Returns a string representation for printing.'''
        st = f"Ego: {self.__ego}\n"
        st+= f"Social Network: {self.__social_network}\n"
        st+= f"Circles: {self.__circles}"
        return st

    __repr__ = __str__
