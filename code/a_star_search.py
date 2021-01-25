#! /usr/bin/env python

import csv
import os

#class for node
class Node:
    def __init__(self, ID, x, y, heuristic_cost_to_go):
        self.id = ID
        self.x = x
        self.y = y
        self.heuristic_cost_to_go = heuristic_cost_to_go
        self.parent = None
        self.past_cost = 100
        self.est_total_cost = None

#class for edge
class Edge:
    def __init__(self, ID1, ID2, cost):
        self.id1 = ID1
        self.id2 = ID2
        self.cost = cost

nodes_list = []
edges_list = [] #aka cost[node1, node2] from the book
OPEN = []
CLOSED = []

#needed to read and write csv
cur_path = os.path.dirname(__file__)
new_path_nodes = os.path.relpath('..\\result\\nodes.csv', cur_path)
new_path_edges = os.path.relpath('..\\result\\edges.csv', cur_path)
new_path_path = os.path.relpath('..\\result\\path.csv', cur_path)

#read nodes.csv, construct node objects and add to the node list
#with open('csv_io/nodes.csv', newline='') as nodes:
with open(new_path_nodes, newline='') as nodes:
    nodes_reader = csv.reader(nodes)
    for row in nodes_reader:
        if row[0][0] == '#': #skip the strings with comments
            continue
        else:
            node_id = int(row[0])
            node_x = float(row[1])
            node_y = float(row[2])
            node_heuristic_cost_to_go = float(row[3])
            nodes_list.append(Node(node_id, node_x, node_y, node_heuristic_cost_to_go))

#read edges.csv, construct edge objects and add to the edge list
with open(new_path_edges, newline='') as edges:
    edges_reader = csv.reader(edges)
    for row in edges_reader:
        if row[0][0] == '#': #skip the strings with comments
            continue
        else:
            edge_id1 = int(row[0])
            edge_id2 = int(row[1])
            edge_cost = float(row[2])
            edges_list.append(Edge(edge_id1, edge_id2, edge_cost))

#finction for writing a path to the path.csv
def write_csv_path(path):
    with open(new_path_path, mode='w') as path_file:
        path_writer = csv.writer(path_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        path_writer.writerow(path)


start_node = 1
end_node = 12

#---------A* algorithm implementation-------------
#Initialization
OPEN.append(nodes_list[0]) #OPEN = {1}
nodes_list[0].past_cost = 0 #past_cost[1] = 0, past_cost[node] = infinity for node {2...N}

while len(OPEN) > 0: #while OPEN is not empty do
    current = OPEN[0] #current = first node in OPEN
    OPEN.remove(current) #remove from OPEN
    CLOSED.append(current.id) #add current to CLOSED
    if current.id == end_node: #if current is in the goal set then
        success = True #return SUCCESS
        print('Success =', success)
        #reconstructing path
        path = []
        while current.id != 1:
            path.insert(0, current.id)
            current = current.parent
        path.insert(0, 1)    
        print('The shortest path is:', path)
        write_csv_path(path)
        break
        
    else:
        for e in edges_list: #for each nbr of current 
            if e.id2 == current.id and e.id1 not in CLOSED: #not in CLOSED do
                tentative_past_cost = current.past_cost + e.cost #tentative_past_cost = past_cost[current]+cost[current,nbr]
                for nbr in nodes_list: 
                    if nbr.id == e.id1:
                        if tentative_past_cost < nbr.past_cost: #if tentative past cost < past cost[nbr] then
                            nbr.past_cost = tentative_past_cost #past_cost[nbr] = tentative_past_cost
                            nbr.parent = current #parent[nbr] = current
                            nbr.est_total_cost = nbr.past_cost + nbr.heuristic_cost_to_go 
                            if nbr not in OPEN:
                                OPEN.append(nbr) #add nbr to the OPEN list
                                OPEN.sort(key=lambda x: x.est_total_cost, reverse=False) #sort the OPEN list by est_total_cost