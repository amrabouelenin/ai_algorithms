# importing required libraries
import numpy as np
import networkx as nx
import math

############## Dijkstra Algorithm ##########

def Dijkstra(graph_dict):
    i = 0
    condition = True
    current_city = 0
    # to keep track of cities we had visited
    visited = []

    # to keep track of cities we havn't visited yet
    unvisited = list(city_names)

    # start from city = 0
    start = 0

    # distances from start to all vericies
    distances = []

    # previous cities
    prev_cities = []

    # initilize the algorithem by setting the distance from the start city to all other city

    for city in graph_dict:
        # set distance for all cities starting from inifity
        if city == 0:
            # set distance from the start city to itself to zero
            distances.append(0)
        else:
            distances.append(math.inf)

    shortest_path = []

    while(unvisited):

        current_neighbors = graph_dict[current_city]
        if i == 10:
            condition = False
        i = i+1
        # set smallest distance temp
        smallest_distance = math.inf
        temp_city = 0
        for neighbor in current_neighbors:
            if neighbor not in visited:
                # remove 0 if it is in the current nebour
                if start in current_neighbors:
                    current_neighbors.remove(start)
                # calculate the distance between the temp city and the start
                new_distance = calculate_distance(start, neighbor,cities_xyz_coordinates)
                if distances[neighbor] > new_distance:
                    distances[neighbor] = new_distance
                # select the city with smallest distance to be the start
                if new_distance < smallest_distance:
                    smallest_distance = new_distance
                    temp_city = neighbor
                    # update the previous vertices - cities
                    prev_cities.append([neighbor, current_city])
                    print('Shortest path distance list', distances)
                    print('Visited',visited)
                    print('Previous vertices',prev_cities)

        # mark the current city as visited
        shortest_path.append(current_city)
        visited.append(current_city)
        if current_city in unvisited:
            unvisited.remove(current_city)
        current_city = temp_city

    shortest_path.append(start)

################################### Helper Functions #######################################################

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

Dijkstra(cities_dict)
