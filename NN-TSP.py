# These are the steps of the algorithm:
# 1. Initialize all vertices as unvisited.
# 2. Select an arbitrary vertex, set it as the current vertex u. Mark u as visited.
# 3. Find out the shortest edge connecting the current vertex u and an unvisited vertex v.
# 4. Set v as the current vertex u. Mark v as visited.
# 5. If all the vertices in the domain are visited, then terminate. Else, go to step 3.

# importing required libraries
import numpy as np
import networkx as nx
import math

#### NN algorithm ####
def NN_algorithm(graph_dict, cities_xyz_coordinates):
    visited = [] # keep track of visited cities
    current = 0  # current index city to explore
    final_path = [0] # final path initial has the start node
    start_node = 0 # start node
    tour = []  # the current tour from current city to neighbor
    temp_current = 0
    while(len(visited) <=len(graph_dict)):
        print('current city', current)
        neighbours = graph_dict[current]
        if start_node in neighbours:
            neighbours.remove(start_node)
        min_distance = np.inf
        for neighbour in neighbours:
            if neighbour not in visited:
                e_distance = calculate_distance(current,neighbour,cities_xyz_coordinates)
                if min_distance > e_distance:
                    min_distance = e_distance
                    tour = neighbour
                    temp_current = neighbour
        final_path.append(tour)
        if (len(final_path) == len(graph_dict)):
            final_path.append(start_node)
            print('Completed path ##########', final_path)
            total_cost = travel_cost(final_path, cities_xyz_coordinates)
            print (' with total cost',total_cost)
            break
        visited.append(current)
        current = temp_current
        print('final_path',final_path)
        print('visited',visited)

########################################## Helper functions ##############################

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

# This is an Euclidean function to calculate the cost of traveling between two cities
# according to the following rule:
# if the plan moves from top to bottom and bottom to up as per #+10%, going down: -10%)
def calculate_distance (start, destination, cities_xyz_coordinates):
    cost = 0
    Euclidean_distance = math.sqrt(((cities_xyz_coordinates[start][0]-cities_xyz_coordinates[destination][0])**2)+((cities_xyz_coordinates[start][1]-cities_xyz_coordinates[destination][1])**2))

    # check if the plane is flying for higher position to lower one. 
    if (cities_xyz_coordinates[start][2] > cities_xyz_coordinates[destination][2]): 
        z_cost = Euclidean_distance + (Euclidean_distance * .10)
        print ("flyiing down  from city {} to city  {} with total distance {}". format( start, destination, z_cost))
    # the plain is flying from bottom to higher position
    else:
        z_cost = Euclidean_distance - (Euclidean_distance * .10)
        print ("flyiing up  from city {} to city  {} with total distance {}". format( start, destination, z_cost))
    
    cost += z_cost
    return cost

# This is an Euclidean function to calculate the cost of traveling between two cities
# according to the following rule:
# if the plan moves from top to bottom and bottom to up as per #+10%, going down: -10%)
def travel_cost(path, cities_xyz_coordinates):
    cost = 0
    for i in path:
        if i == len(path):
            break
        start = path[i]
        destination = path[i+1]
        Euclidean_distance = math.sqrt(((cities_xyz_coordinates[start][0]-cities_xyz_coordinates[destination][0])**2)+((cities_xyz_coordinates[start][1]-cities_xyz_coordinates[destination][1])**2))

        # check if the plane is flying for higher position to lower one. 
        if (cities_xyz_coordinates[start][2] > cities_xyz_coordinates[destination][2]): 
            z_cost = Euclidean_distance + (Euclidean_distance * .10)
            print ("flyiing down  from city {} to city  {} with total distance {}". format( start, destination, z_cost))
        # the plain is flying from bottom to higher position
        else:
            z_cost = Euclidean_distance - (Euclidean_distance * .10)
            print ("flyiing up  from city {} to city  {} with total distance {}". format( start, destination, z_cost))
        cost += z_cost
    return cost

########################################## Initializing the problem parameters ##############################

# number of cities
n = 5
xy_coorindates_lower_limit = -100
xy_coorindates_upper_limit = 100
# generating x,y points between -100, 100 for n cities as an initial values.
# -100, 100 are requirement, it can be modfieid
cities_xy_coorindates = np.random.randint(xy_coorindates_lower_limit,xy_coorindates_upper_limit, size=(n, 2))

# geneating z to represent the plan height from the ground as the salesman is using plane.
z_coorindates_lower_limit = -50
z_coorindates_upper_limit = 50
cities_z_coordinates = np.random.randint(z_coorindates_lower_limit,z_coorindates_upper_limit, size=(n, 1))

# concatinating cities_xyz_coordinates matercs
cities_xyz_coordinates = np.concatenate((cities_xy_coorindates, cities_z_coordinates), axis=1)

# give city names number 
city_names = np.arange(n)

# create cities with their corresponding corridintates
cities = np.concatenate((city_names.reshape(n,1), cities_xy_coorindates), axis=1)

# generate full map with distances
cities_map = genearte_cities_map(cities)

# store map coordinates of the cities in dictionary
cities_dict = create_cities_dict(cities_map)

NN_algorithm(cities_dict, cities_xyz_coordinates)