###These are the steps of the algorithm:

# 1. Initialize all vertices as unvisited.

# 2. Select an arbitrary vertex, set it as the current vertex u. Mark u as visited.

# 3. Find out the shortest edge connecting the current vertex u and an unvisited vertex v.

# 4. Set v as the current vertex u. Mark v as visited.

# 5. If all the vertices in the domain are visited, then terminate. Else, go to step 3.

import numpy as np
import pandas as pd
import math

# calculate distance between two citieis
def calc_distance (city1, city2, xyz):
    total_cost = 0
    Euclidean_distance = math.sqrt(((xyz[city1][0]-xyz[city2][0])**2)+((xyz[city1][1]-xyz[city2][1])**2))
    if (xyz[city1][2] > xyz[city2][2]): #means that the plane is travleing from bottom to top
        total_cost_z = Euclidean_distance + (Euclidean_distance * .10)
    else:
        total_cost_z = Euclidean_distance - (Euclidean_distance * .10)
    total_cost = total_cost + total_cost_z
    return total_cost

# calculate full path distance
def calc_cost_path (complete_path, xyz):
    total_cost = 0

    #complete_path = [0, 2, 3, 4, 1, 0]
    for i in complete_path:
        if i == len(complete_path):
            break
        city1 = complete_path[i]
        city2 = complete_path[i+1]
        xyz[city1]
        print
        Euclidean_distance = math.sqrt(((xyz[city1][0]-xyz[city2][0])**2)+((xyz[city1][1]-xyz[city2][1])**2))
        print ("distance between city {} and city {} is {}". format( city1, city2, Euclidean_distance))
        if (xyz[city1][2] > xyz[city2][2]): #means that the plane is travleing from bottom to top
            total_cost_z = Euclidean_distance + (Euclidean_distance * .10)
            print ("flyiing down  from city {} to city  {} with total distance {}". format( city1, city2, total_cost_z))
        else:
            total_cost_z = Euclidean_distance - (Euclidean_distance * .10)
            print ("flyiing up  from city {} to city  {} with total distance {}". format( city1, city2, total_cost_z))

        total_cost = total_cost + total_cost_z

    return total_cost

##### Driver Code #####
# generating x,y points between -100, 100 for 5 cities an initial values.
xy = np.random.randint(-100,100, size=(5, 2))
# geneating z to represent the plan height from the ground
z = np.random.randint(-50,50, size=(5, 1))
# concatinating xyz matercs
xyz = np.concatenate((xy, z), axis=1)
# give city names number from 0 to 4
city_names = np.arange(5)
# create cities with their corresponding corridintates
cities = np.concatenate((city_names.reshape(5,1), xy), axis=1)
## storing all connection in dictionary

graph_dict = {
0 : [1, 2, 3],
1 : [0, 2, 3, 4],
2 : [0, 1, 3],
3 : [0, 1, 2, 4],
4: [1, 3]}

#### NN algorithm ####
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
            e_distance = calc_distance(current,neighbour,xyz)
            if min_distance > e_distance:
                min_distance = e_distance
                tour = neighbour
                temp_current = neighbour
    final_path.append(tour)
    if (len(final_path) == len(graph_dict)):
        final_path.append(start_node)
        print('Completed path ##########', final_path)
        total_cost = calc_cost_path(final_path, xyz)
        print (' with total cost',total_cost)
        break
    visited.append(current)
    current = temp_current
    print('final_path',final_path)
    print('visited',visited)
