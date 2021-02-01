# Import libraries
import numpy as np
import math

# to build a graph of cities
import networkx as nx

# generate random points for x,y between -100, 100
xy = np.random.randint(-100,100, size=(5, 2))

# generate random hight values for the plan between -50, 50
z = np.random.randint(-50,50, size=(5, 1))

# concatinate all coorindates in one array for later retrival of information
xyz = np.concatenate((xy, z), axis=1)

# generate 5 city names as 0,1,2, ..
city_names = np.arange(5)

# link city names with it's coorindates
cities = np.concatenate((city_names.reshape(5,1), xy), axis=1)

# prepare a graph with edges for the cities
G=nx.Graph()
i = 0
for city in cities:
     G.add_node(cities[i,0],pos=tuple(cities[i,1:].astype(int)))
     i = i+1

edges_list = []
for city in cities:
    for city_temp in cities:
        if city_temp[0] != city[0]:
            Euclidean_distance = math.sqrt(((city[1]-city_temp[1])**2)+((city[2]-city_temp[2])**2))
            #G.add_edge(city[0], city_temp[0],weight = 5)
            G.add_edge(city[0], city_temp[0],weight = round(Euclidean_distance,0))
            edges_list.append((city[0], city_temp[0]))
# to have 80% possible connection
G.remove_edge(0,4)
G.remove_edge(2,4)

# create dictionary to save every city with it's neighbors
graph_dict = {}
for (city1, city2) in G.edges:
    if city1 in graph_dict:
        graph_dict[city1].append(city2)
    else:
        graph_dict[city1] = [city2]
    if city2 in graph_dict:
        graph_dict[city2].append(city1)
    else:
        graph_dict[city2] = [city1]


# function to calculate the totl cost of the completed final_path#+10%, going down: -10%)

def calc_cost_path (complete_path, xyz):
    total_cost = 0
    print(complete_path)
    #complete_path = [0, 2, 3, 4, 1, 0]
    for i in range(0,len(complete_path)-1):

        if i == len(complete_path):
            break
        city1 = complete_path[i]
        city2 = complete_path[i+1]

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

  # Calculate the distance between two cities if z1 is less than z2 from city one to city two
  # then it decrease distance by -10% else increased the distance by 10% of the total cost
def calc_distance (city1, city2, xyz):

    total_cost = 0

    Euclidean_distance = math.sqrt(((xyz[city1][0]-xyz[city2][0])**2)+((xyz[city1][1]-xyz[city2][1])**2))

    # if the plane is flying down to city2
    if (xyz[city1][2] > xyz[city2][2]):

        total_cost_z = Euclidean_distance - (Euclidean_distance * .10)

    # the plane if flying up to city2
    else:
        total_cost_z = Euclidean_distance + (Euclidean_distance * .10)

    total_cost = total_cost + total_cost_z
    return total_cost


    # driver Code
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
            new_distance = calc_distance(start, neighbor,xyz)
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
