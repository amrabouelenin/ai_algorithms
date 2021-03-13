# importing required libraries
import numpy as np
import networkx as nx
import math

############# Bredth First Algorithm ################

def BFS_TSP(cities_map, start):
    paths = []
    visited = []
    start = 0
    queue = []
    final_paths = []

    # geneare the root paths
    children = cities_map[start]
    for child in children:
        paths.append([start,child])
        queue.append([start,child])

    i = 0
    while(len(queue)):
        path = queue.pop(0)
        city = path[-1]
        children = cities_map[city]
        city_path = city_has_path(city, paths)
        print("Exploring city #", city)
        for child in children:
            if child != start:
                if(city_path):
                    new_path = city_path.copy()
                    # check if the child not in the path
                    if (child not in new_path):
                        new_path.append(child)
                        print (new_path)
                        queue.append(new_path)
                        paths.append(new_path)
                        if (len(new_path) == 5):
                            node = new_path[-1]
                            if start in cities_map[node]:
                                new_path.append(start)
                                print('Completed path ##########', new_path)
                                total_cost = travel_cost(new_path, xyz)
                                print (' with total cost',total_cost)
                                final_paths.append([new_path,total_cost])
                            else:
                                pass
                                print('CANCELED path', new_path)

        i = i+1
        #remove the path of this city add the new paths
        paths.remove(city_path)
    return final_paths;


################################### Helper Functions #######################################################

# This is an Euclidean function to calculate the cost of traveling between two cities
# according to the following rule:
# if the plan moves from top to bottom and bottom to up as per #+10%, going down: -10%)
def travel_cost(path, xyz):
    cost = 0
    for i in path:
        if i == len(path):
            break
        start = path[i]
        destination = path[i+1]
        Euclidean_distance = math.sqrt(((xyz[start][0]-xyz[destination][0])**2)+((xyz[start][1]-xyz[destination][1])**2))

        # check if the plane is flying for higher position to lower one. 
        if (xyz[start][2] > xyz[destination][2]): 
            z_cost = Euclidean_distance + (Euclidean_distance * .10)
        # the plain is flying from bottom to higher position
        else:
            z_cost = Euclidean_distance - (Euclidean_distance * .10)
        cost += z_cost
    return cost

def city_has_path(city, paths):
    for path  in paths:
        if path[-1] == city:
            return path
    return False

########################################## Initializing the problem parameters ##############################

# number of cities
n = 5

# generating x,y points between -100, 100 for n cities as an initial values.
xy = np.random.randint(-100,100, size=(n, 2))

# geneating z to represent the plan height from the ground as the salesman is using plane.
z = np.random.randint(-50,50, size=(n, 1))

# concatinating xyz matercs
xyz = np.concatenate((xy, z), axis=1)

# give city names number 
city_names = np.arange(n)

# create cities with their corresponding corridintates
cities = np.concatenate((city_names.reshape(n,1), xy), axis=1)

# maping the cities coordinates into a network of graph for better visualization
# removing edges/routes between cities if nessacary according to requirement

def genearte_cities_map(cities):
    # intialize cities_map
    cities_map = nx.Graph()
    i = 0
    for city in cities:
        cities_map.add_node(cities[i,0],pos=tuple(cities[i,1:].astype(int)))
        i = i+1

    edges_list = []
    for city in cities:
        for city_temp in cities:
            if city_temp[0] != city[0]:

                Euclidean_distance = math.sqrt(((city[1]-city_temp[1])**2)+((city[2]-city_temp[2])**2))
                cities_map.add_edge(city[0], city_temp[0],weight = round(Euclidean_distance,0))
                edges_list.append((city[0], city_temp[0]))

    # to have 80% possible connection
    cities_map.remove_edge(0,4)
    cities_map.remove_edge(2,4)
    return cities_map

# store final cities information in a dictionary
def create_cities_dict(cities_map):
    cities_dict = {}
    for (start, destination) in cities_map.edges:
        if start in cities_dict:
            cities_dict[start].append(destination)
        else:
            cities_dict[start] = [destination]
        if destination in cities_dict:
            cities_dict[destination].append(start)
        else:
            cities_dict[destination] = [start]
    return cities_dict

# generate full map with distances
cities_map = genearte_cities_map(cities)
# store map coordinates of the cities in dictionary
cities_dict = create_cities_dict(cities_map)

#################################### RUN the Algorithm #################################################
# run the algorithm with start node 0
final_paths = BFS_TSP(cities_dict, 0)

# list the pathes in a sorted order
sorted(final_paths, key=lambda x: x[1])