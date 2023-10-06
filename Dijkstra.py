INF = 1000000

class DHeapNode:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance

def d_heap_parent(i, d):
    return (i - 1) // d

def d_heap_child(d, index, pos):
    return index * d + (pos + 1)

def d_heap_up(d, heap, i):
    while i > 0:
        parent_index = d_heap_parent(i, d)
        if heap[i].distance < heap[parent_index].distance:
            heap[i], heap[parent_index] = heap[parent_index], heap[i]
            i = parent_index
        else:
            break

def d_heap_down(d, heap, i, size):
    while True:
        min_index = i
        for j in range(1, d + 1):
            child_index = d_heap_child(d, i, j)
            if child_index < size and heap[child_index].distance < heap[min_index].distance:
                min_index = child_index

        if min_index != i:
            heap[i], heap[min_index] = heap[min_index], heap[i]
            i = min_index
        else:
            break

def dijkstra(graph, start):
    num_nodes = len(graph)
    distances = [INF] * num_nodes
    distances[start] = 0

    d = 2  # You can adjust the D value here

    d_heap = [DHeapNode(i, distances[i]) for i in range(num_nodes)]
    d_heap_index = {node.name: i for i, node in enumerate(d_heap)}

    while d_heap:
        current_node = d_heap[0].name
        current_distance = d_heap[0].distance
        d_heap[0] = d_heap[-1]
        d_heap.pop()
        d_heap_down(d, d_heap, 0, len(d_heap))

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                i = d_heap_index[neighbor]

                if i < len(d_heap):
                    d_heap[i].distance = distance
                    d_heap_up(d, d_heap, i)
                else:
                    d_heap.append(DHeapNode(neighbor, distance))
                    d_heap_index[neighbor] = len(d_heap) - 1
                    d_heap_up(d, d_heap, len(d_heap) - 1)

    return distances

# Sample graph represented as an adjacency list
# Format: (node, weight)
graph = [
    [(1, 2), (2, 4)],
    [(0, 2), (2, 1), (3, 7)],
    [(0, 4), (1, 1), (3, 3), (4, 5)],
    [(1, 7), (2, 3), (4, 2)],
    [(2, 5), (3, 5)]
]


start_node = 0
distances = dijkstra(graph, start_node)

for i, distance in enumerate(distances):
    if distance == INF:
        print(f"{i}         Unreachable")
    else:
        print(f"{i}         {distance}")
