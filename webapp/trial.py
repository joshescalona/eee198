from pqdict import PQDict
import pickle

# load adjacency list object
def load_object(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def dijkstra_endlist(adjacency_list, start, nodelist):
    graph = adjacency_list
    match_node = 0
    inf = float('inf')
    shortest_distances = {start: 0}                 # mapping of nodes to their dist from start
    queue_sd = PQDict(shortest_distances)           # priority queue for tracking min shortest path
    predecessors = {}                               # mapping of nodes to their direct predecessors
    unexplored = set(graph.keys())                  # unexplored nodes
    path = []

    while unexplored:                                           # nodes yet to explore
        try:
          (minNode, minDistance) = queue_sd.popitem()             # node w/ min dist d on frontier
        except KeyError:
          print('Path not reachable')
          return None, None, None
        shortest_distances[minNode] = minDistance               # est dijkstra greedy score
        unexplored.remove(minNode)                              # remove from unexplored
        if minNode in nodelist:
             match_node = minNode
             break                                              # end if goal already reached

        # now consider the edges from minNode with an unexplored head -
        # we may need to update the dist of unexplored successors
        for neighbor in graph[minNode]:
            if neighbor in unexplored:
                minDistance = shortest_distances[minNode] + graph[minNode][neighbor]
                if minDistance < queue_sd.get(neighbor, inf):
                    queue_sd[neighbor] = minDistance
                    predecessors[neighbor] = minNode                   # set/update predecessor

    currentNode = match_node
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessors[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distances[match_node] != inf:
        return shortest_distances[match_node], path, match_node


if __name__ == '__main__':
  adjacency_list = load_object('adj_list_obj.pkl')
  source = '7014239115'
  node_list = ['1802505590']
  print(node_list)
  shortest_distance, path, matched_node = dijkstra_endlist(adjacency_list, source, node_list)
