# importing required libraries
import numpy as np
import pandas as pd
from mpl_toolkits import mplot3d
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
import networkx as nx
import math

def BFS_TSP(graph_dict, start):
    paths = []
    visited = []
    start = 0
    queue = []
    final_paths = []
    # geneare the root paths
    children = graph_dict[start]
    for child in children:
        paths.append([start,child])
        queue.append([start,child])

    i = 0
    while(len(queue)):
        path = queue.pop(0)
        city = path[-1]
        children = graph_dict[city]
        city_path = city_has_path(city, paths)
        print("exploring city", city)
        for child in children:
            if child != start:
                #print("adding", child)
                #print("city path", city_path)
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
                            if start in graph_dict[node]:
                                new_path.append(start)
                                print('Completed path ##########', new_path)
                                total_cost = calc_cost_path(new_path, xyz)
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

# cost of the path from city to another considering the hight of the plane
# if it moves from top to bottom and bottom to up as per #+10%, going down: -10%)
def calc_cost_path (complete_path, xyz):
    total_cost = 0
    for i in complete_path:
        if i == len(complete_path):
            break
        city1 = complete_path[i]
        city2 = complete_path[i+1]
        Euclidean_distance = math.sqrt(((xyz[city1][0]-xyz[city2][0])**2)+((xyz[city1][1]-xyz[city2][1])**2))
        if (xyz[city1][2] > xyz[city2][2]): #means that the plane is travleing from bottom to top
            total_cost_z = Euclidean_distance + (Euclidean_distance * .10)
        else:
            total_cost_z = Euclidean_distance - (Euclidean_distance * .10)
        total_cost = total_cost + total_cost_z

    return total_cost

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


############################ Draw the problem according to requirments ############################

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
            G.add_edge(city[0], city_temp[0],weight = round(Euclidean_distance,0))
            edges_list.append((city[0], city_temp[0]))

# to have 80% possible connection
G.remove_edge(0,4)
G.remove_edge(2,4)
pos=nx.get_node_attributes(G,'pos')
nx.draw(G,pos,node_size=1000,node_color='blue',alpha=0.9,labels={node:node for node in G.nodes()})
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

# 3d visiualization for the possible positions of the plan for every city
xyz_df = pd.DataFrame(xyz)
xyz_df.rename(columns={0: 'x', 1: 'y',  2:'z'}, inplace=True)
xyz_df
px.scatter_3d()
fig = px.scatter_3d(xyz_df, x='x', y='y', z='z')
fig.show()

####################################### store final city information in Dictionary ######################

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

#################################### RUN the Algorithm #################################################
# run the algorithm with start node 0
final_paths = BFS_TSP(graph_dict, 0)

# list the pathes in a sorted order
sorted(final_paths, key=lambda x: x[1])
