import xlrd
from queue import Queue
from recordtype import recordtype

Edge = recordtype('Edge', ['nextNode', 'reverseIndex', 'flow', 'cap'])

nextNodeIndex = list()
level = list()
MAXVAL = 1000000000

LOG_STEPS = True
FILE_LOCATION = "C:/Users/eledah/Documents/Uni/tpmaxflow-py/data/d4.xlsx"


def step_log(txt):
    if LOG_STEPS:
        print("STEP:", txt)


def addEdge(prevNode, nextNode, weight, graph):
    forward = Edge(nextNode, len(graph[nextNode]), 0, weight)
    backward = Edge(prevNode, len(graph[prevNode]), 0, weight)

    graph[prevNode].append(forward)
    graph[nextNode].append(backward)


def bfs(srcNode, destNode, graph):
    for index in range(len(level)):
        level[index] = -1

    q = Queue()
    q.put(srcNode)
    level[srcNode] = 0

    while q.qsize() > 0:
        currNode = q.get()

        for i in range(0, len(graph[currNode])):
            currEdge = graph[currNode][i]
            nextNode = currEdge.nextNode

            if level[nextNode] == -1 and currEdge.flow < currEdge.cap:
                level[nextNode] = level[currNode] + 1
                q.put(nextNode)

    return level[destNode] != -1


def dfs(currNode, destNode, currMinFlow, graph):
    if currNode == destNode:
        return currMinFlow

    # for nextNodeIndex[currNode] in range(nextNodeIndex[currNode], len(graph[currNode])):
    for nextNodeIndex[currNode] in range(nextNodeIndex[currNode], len(graph[currNode])):
        e = graph[currNode][nextNodeIndex[currNode]]

        if level[e.nextNode] == level[currNode] + 1 and e.flow < e.cap:
            nextFlow = min(currMinFlow, e.cap - e.flow)
            dfsVal = dfs(e.nextNode, destNode, nextFlow, graph)

            if dfsVal > 0:
                e.flow += dfsVal
                graph[e.nextNode][e.reverseIndex].flow -= dfsVal
                return dfsVal

    return 0


def maxFlow(src, dest, graph):
    totalFlow = 0

    while bfs(src, dest, graph):
        for index in range(len(nextNodeIndex)):
            nextNodeIndex[index] = 0
        flow = dfs(src, dest, MAXVAL, graph)
        while flow:
            totalFlow += flow
            flow = dfs(src, dest, MAXVAL, graph)

    return totalFlow

graph = list()
step_log("Adding edges.")

# MANUAL INPUT METHOD
# numNodes = int(input("Enter the number of nodes:"))
# numEdges = int(input("Enter the number of edges:"))

# for i in range(0, numEdges):
#     graph.append(list())

# for i in range(0, numNodes):
#     level.append(0)
#     nextNodeIndex.append(0)

# for i in range(0, numEdges):
#     a = int(input())
#     b = int(input())
#     c = int(input())
#
#     a -= 1
#     b -= 1
#     addEdge(a, b, c, graph)
#     print("Edge added!")

# SIMPLE EXAMPLE
# numNodes = 4
# numEdges = 6

# for i in range(0, numEdges):
#     graph.append(list())

# for i in range(0, numNodes):
#     level.append(0)
#     nextNodeIndex.append(0)

# addEdge(0, 1, 3, graph)
# addEdge(1, 2, 4, graph)
# addEdge(2, 0, 2, graph)
# addEdge(1, 1, 5, graph)
# addEdge(2, 3, 3, graph)
# addEdge(3, 2, 3, graph)

# READING DATA FROM EXCEL FILE
wb = xlrd.open_workbook(FILE_LOCATION)
sheet = wb.sheet_by_index(0)

numNodes = int(sheet.cell_value(0, 0))
numEdges = int(sheet.cell_value(0, 1))
for i in range(0, numNodes):
    level.append(0)
    nextNodeIndex.append(0)
for i in range(0, numEdges):
    graph.append(list())

for i in range(1, sheet.nrows):
    src = int(sheet.row_values(i)[0] - 1)
    dest = int(sheet.row_values(i)[1] - 1)
    weight = int(sheet.row_values(i)[2])
    addEdge(src, dest, weight, graph)

step_log("All edges added.")
step_log("Starting calculations.")

MAXFLOW = maxFlow(0, numNodes - 1, graph)

step_log("Calculations done!")

print("Maximum Possible Flow: ", MAXFLOW)
