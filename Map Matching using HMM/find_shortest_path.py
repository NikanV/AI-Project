import numpy as np
import pandas as pd
import heapq

def get_node_id(pos, graph):
    u_node = graph.loc[(graph["u_lat"] == pos[0]) & (graph["u_lon"] == pos[1])].to_numpy()
    v_node = graph.loc[(graph["v_lat"] == pos[0]) & (graph["v_lon"] == pos[1])].to_numpy()
    if len(u_node) > 0:
        return u_node[0][1]
    else:
        return v_node[0][2]

def get_neighbors(node, graph):
    nodes_to = graph.loc[(graph["u"] == node)].to_numpy()
    nodes_from = graph.loc[(graph["v"] == node)].to_numpy()
    return [(row[2], row[3]) for row in nodes_to] + [(row[1], row[3]) for row in nodes_from]

def backtrack(curr_node, parents):
    return [curr_node] if parents[curr_node] is None else backtrack(parents[curr_node], parents) + [curr_node]

# TODO: You should implement this from scratch and you cannot use any library (such as networkx) for finding the shortest path.
def find_shortest_path(start_node, end_node, graph):
    """
    Find the shortest path between two nodes in a graph.
    :param start_node: The start node
    :param end_node: The end node
    :param graph: The graph
    :return: The shortest path. It is a list of node_ids from start_node to end_node.
    Note that you use all of the data in "pasdaran_streets" dataset appropriately such as "street_length" and "one_way".
    """
    start_node_id = get_node_id(start_node, graph)
    end_node_id = get_node_id(end_node, graph)
    heap = []
    costs = {}
    parents = {}
    route = []
    
    heapq.heappush(heap, (0, start_node_id))
    costs[start_node_id] = 0
    parents[start_node_id] = None
    
    while heap:
        _, curr_node = heapq.heappop(heap)
        if curr_node == end_node_id:
            route = backtrack(curr_node, parents)
            break
        for neighbor, distance in get_neighbors(curr_node, graph):
            if neighbor not in costs or costs[neighbor] > costs[curr_node] + distance:
                costs[neighbor] = costs[curr_node] + distance
                parents[neighbor] = curr_node
                heapq.heappush(heap, (costs[neighbor], neighbor))
    
    return route