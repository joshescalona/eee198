from pqdict import PQDict
import pickle

# load adjacency list object
def load_object(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def dijkstra(graph, start, end):
    inf = float('inf')
    shortest_distances = {start: 0}                 # mapping of nodes to their dist from start
    queue_sd = PQDict(shortest_distances)           # priority queue for tracking min shortest path
    predecessors = {}                               # mapping of nodes to their direct predecessors
    unexplored = set(graph.keys())                  # unexplored nodes
    path = []

    while unexplored:                                           # nodes yet to explore
        (minNode, minDistance) = queue_sd.popitem()             # node w/ min dist d on frontier
        shortest_distances[minNode] = minDistance               # est dijkstra greedy score
        unexplored.remove(minNode)                              # remove from unexplored
        if minNode == end: break                                # end if goal already reached

        # now consider the edges from minNode with an unexplored head -
        # we may need to update the dist of unexplored successors
        for neighbor in graph[minNode]:                               # successors to v
            if neighbor in unexplored:                          # then neighbor is a frontier node
                minDistance = shortest_distances[minNode] + graph[minNode][neighbor]
                if minDistance < queue_sd.get(neighbor, inf):
                    queue_sd[neighbor] = minDistance
                    predecessors[neighbor] = minNode                   # set/update predecessor

    currentNode = end
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessors[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distances[end] != inf:
        return shortest_distances[end], path


def shortest_path(G, start, end):
    dist, pred = dijkstra(G, start, end)
    v = end
    path = [v]
    while v != start:
        v = pred[v]
        path.append(v)
    path.reverse()
    return path


if __name__ == '__main__':

    # graph = {'a': {'b': 14, 'c': 9, 'd': 7},
    #          'b': {'a': 14, 'c': 2, 'e': 9},
    #          'c': {'a': 9, 'b': 2, 'd': 10, 'f': 11},
    #          'd': {'a': 7, 'c': 10, 'f': 15},
    #          'e': {'b': 9, 'f': 6},
    #          'f': {'c': 11, 'd': 15, 'e': 6}}

    # dist, pred = dijkstra(graph, 'a', 'f')
    # print(dist)
    # print(pred)
    # expected = {'a': 0, 'c': 9, 'b': 11, 'e': 20, 'd': 7, 'f': 20}
    # assert dist == expected

    # store loaded object to variable
    adj_list = load_object("adj_list_obj.pkl")

    # graph = {'a':{'b':10,'c':3},'b':{'c':1,'d':2},'c':{'b':4,'d':8,'e':2},'d':{'e':7},'e':{'d':9}}
    dist, pred = dijkstra(adj_list, '17216409', '5369579207')
    print(dist)
    print(pred)
