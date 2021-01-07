from EgoNet import EgoNet
from Node import Node
from Feature import Feature
from Circle import Circle
from operator import itemgetter

def get_ego_net_files():
    y1 = "_ego_features.txt"
    y2 = "_ego_net_features.txt"
    y3 = "_alters_features.txt"
    y4 = "_ego_net_connections.txt"
    y5 = "_circles.txt"
    x = input("Enter user id to generate EgoNet:")
    while True:
        try:
            fp1 = open(x+y1)
            fp2 = open(x+y2)
            fp3 = open(x+y3)
            fp4 = open(x+y4)
            fp5 = open(x+y5)

            return (int(x),fp1,fp2,fp3,fp4,fp5)

        except FileNotFoundError:
            print("File not found for ego_id: ",x)
            x = input("Enter user id to generate EgoNet: ")

def get_ego_net_features(fp):
    '''Takes file pointer and reads data, returns the dictionary of ego net features'''
    ego_net_features = {}
    
    for line in fp: #reads through each line 
        list_of_strings = line.split()
        key = int(list_of_strings.pop(0)) #takes out the feature name
        feature_id = str(list_of_strings.pop(2)) #grabs the feature id
        list_of_strings[0] = list_of_strings[0].split(";")
        for i in list_of_strings[0]: #removes anonymized from feature name
            if i == "anonymized": 
                list_of_strings[0].remove(i)
            
        for i in list_of_strings[0]:#removes id from feature name
            if i == "id":
                list_of_strings[0].remove(i)
        
            
        
        feature_name = "_".join(list_of_strings[0])
        ego_net_features[key] = (feature_name, feature_id )
        
    return ego_net_features

def add_ego_net_features_to_ego(ego, ego_feature_file, ego_net_features):
    '''Reads a one-line file of features for the ego node'''
    line_list = ego_feature_file.readline().split()    # read one line
    # i is the index, digit is the value
    for i,digit in enumerate(line_list):
        # in order to add a feature we must create a Feature instance
        ego.add_feature(i,Feature(ego_net_features[i][1], ego_net_features[i][0],int(digit)))
    return ego

def add_alters_to_ego_net(ego_net,alter_features_file,ego_net_features):
    '''adding alters from alter_features_file, adds to ego_net'''
    for line in alter_features_file:#reads through each line of file
        line = line.split()
        node_id = line.pop(0)
        alter = Node(int(node_id), (len(line)))#turns node_id into integer and takes the length of the line (number of features)
        for i,digit in enumerate(line): 
            alter.add_feature(i, Feature(ego_net_features[i][1], ego_net_features[i][0], int(digit)))
        ego_net.add_alter_node(alter)
        
    
    
    return ego_net

def add_connections_to_ego_net(ego_net,connections_file):
    '''it finds the connections in between the connections file to ego_net'''
    for line in connections_file: #reads through each line in the file
        line = line.split()
        alter1 = int(line[0]) #takes out both pairs 
        alter2 = int(line[1])
        
        node_1= ego_net.get_alter_node(alter1) #retrieves the alter nodes for both pairs
        node_2 = ego_net.get_alter_node(alter2)
        
        ego_net.add_connection_between_alters(node_1, node_2) #adds the connections between the alters
        
    
    return ego_net

def add_circles_to_ego_net(ego_net,circles_file):
    '''Adds the circles to ego_net'''
    for line in circles_file: #reads through each line of the file
        line = line.split()
        circle_name = line.pop(0) #takes out the circle name
        alter_id = line
        node_circle = set() #intialize set for the alter nodes 
        
        for i in alter_id:
            i = int(i)
            nodeobj = ego_net.get_alter_node(i)
            node_circle.add(nodeobj)
        
        ego_net.add_circle(circle_name, node_circle) #adds the circle object into ego_net
        
    return ego_net

def calculate_circle_similarity(ego_net,circle_name):
    '''This function calculates the similarity of the alters with in the circle, returns the dictionary with keys being the position of features and values as the sum of the values of the corresponding feature'''
    dict1 = {} #creates new dictionary
    features = ego_net.get_ego_net_features()
    
    for position in features: #for loop in features
        values_sum = 0
        circle = ego_net.get_circle(circle_name) #finds the circle
        alter_values = circle.get_alters() #finds the alter values
        
        for alter in alter_values: 
            value = alter.get_feature_value(position)
            values_sum += value 
        
        dict1[position] = values_sum
    
    
    return dict1

def calculate_ego_E_I_index(ego_net,feature_name,feature_id):
    '''Calculates Krackhardt and Stern's EI index'''
    connection_total = len(ego_net.get_alters())
    alter_values = ego_net.get_alters()
    internal = 0
    position = ego_net.get_feature_pos(feature_name, feature_id)
    
    
    for i in alter_values: #goes through each alter 
        value = i.get_feature_value(position)
        internal += value
    
    E = connection_total - internal
     
    e_i_index = (E - internal)/(E + internal) #basic formula for finding E/I Index
    
    
    return float(e_i_index)
    
    
    
def calculate_ego_net_effective_size(ego_net):
    '''Calculates the Effective size of ego_net'''
    total_alters = ego_net.get_alter_node_count()
    
    redundancy = 0 #setting up the count for redundancy
    
    nodeobj = EgoNet.get_alters(ego_net) #gets alters of ego_net
    
    for i in nodeobj: 
        count = ego_net.get_alter_connections(i) 
        redundancy +=  len(count)-1 #counts the number of times of redundancy
        
        
    effective_size = (redundancy-total_alters) / total_alters
    
    size = total_alters - effective_size
    size = size -1 
    
    return float(size)

def calculate_ego_net_efficiency(ego_net):
    '''Calculates the ego_net efficiency which is formula: actual size / effective size '''
    effective_size = calculate_ego_net_effective_size(ego_net) #finds the effective size
    total_alters = EgoNet.get_alter_node_count(ego_net) #finds the alter node count
    
    Efficiency = effective_size / total_alters #divide the effective size by count of nodes 
    
    return float(Efficiency)

def print_choices():
    print("\nChoices for Ego Net calculation: ")
    print("1 - Top 5 similar features in a circle")
    print("2 - Calculate effective size of Ego Net")
    print("3 - Calculate circle E/I index")
    print("4 - Calculate Ego Net efficiency")
    print("q/Q - Quit ")

def main():
    ego_id,ego_feature_file,ego_net_features_file,alter_features_file,connections_file,circles_file=get_ego_net_files()
    ego_net_features = get_ego_net_features(ego_net_features_file)

    ego = Node(ego_id,len(ego_net_features))

    ego = add_ego_net_features_to_ego(ego,ego_feature_file,ego_net_features)

    FacebookNet = EgoNet(ego,ego_net_features)

    FacebookNet = add_alters_to_ego_net(FacebookNet,alter_features_file,ego_net_features)

    FacebookNet = add_connections_to_ego_net(FacebookNet,connections_file)

    FacebookNet = add_circles_to_ego_net(FacebookNet,circles_file)

    while True:
        print_choices()
        choice = input("Enter choice: ").strip()
        circle_names = FacebookNet.get_circle_names()
        if choice == "1":
            circle_name = input("Enter circle name to calculate similarity: ")
            circle_size = (FacebookNet.get_circle(circle_name).get_circle_size())
            if circle_name in circle_names:
                similarity_dict = calculate_circle_similarity(FacebookNet,circle_name)
            else:
                print("Circle name not in Ego Net's circles. Please try again!")
                continue
            similarity_dict = dict(sorted(similarity_dict.items(),key=itemgetter(1),reverse=True)[:5])
            for feature_pos in similarity_dict:
                feature_name_id = FacebookNet.get_ego_net_feature(feature_pos)
                feature_similarity = (similarity_dict[feature_pos])/(circle_size)
                print(f"Feature: {feature_name_id}")
                print(f"Feature Similarity in {circle_name}: {feature_similarity} \n")
            print()
        elif choice == '2':
            print(f"Effective size of the Ego Net is: {calculate_ego_net_effective_size(FacebookNet)}")
            print()
        elif choice == '3':
            feature_name = input("Enter feature name to calculate E/I index: ")
            feature_id = (input(f"Enter id for {feature_name} to calculate E/I index: "))
            e_i_index = calculate_ego_E_I_index(FacebookNet,feature_name,feature_id)
            if e_i_index < 0:
                print(f"Ego is more homophilic for {feature_name}_{feature_id} with an E/I index of {e_i_index}")
                print()
            else:
                print(f"Ego is more heterophilic for {feature_name}_{feature_id} with an E/I index of {e_i_index}")
                print()

        elif choice == '4':
            ego_net_efficiency = calculate_ego_net_efficiency(FacebookNet)
            print("The efficiency of the Ego Net is: {:.2f}%".format(100*ego_net_efficiency))
            print()

        elif choice in 'qQ':
            break
        else:
            print("Incorrect Choice. Please try again.")
            continue
    ego_feature_file.close()
    ego_net_features_file.close()
    alter_features_file.close()
    connections_file.close()

if __name__ == "__main__":
   main()
