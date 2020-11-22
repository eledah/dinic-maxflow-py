import xlrd
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
from recordtype import recordtype

# Configurations
LOG_STEPS = True

# Drawing Config
DRAW_INITIAL_GRAPH = True
DRAW_ITERATION_GRAPH = True
DRAW_FINAL_GRAPH = True
GRAPH_RESIZE = True
GRAPH_SIZE = 5
SAVE_GRAPHS = False

# File Config
FILE_LOCATION_ROOT = "C:/Users/eledah/Documents/Uni/tpmaxflow-py/"
FILE_LOCATION_DATA = "data/d2.xlsx"
FILE_LOCATION_GRAPHS = "output/visual/"

# Color Config
NODE_SOURCE = "#E91E63"
NODE_SINK = "#388E3C"
NODE_DEFAULT = "#03A9F4"
EDGE_OVERLOADED = "#b71c1c"
EDGE_DEFAULT = "#616161"

# Tools
Edge = recordtype('Edge', ['nextNode', 'reverseIndex', 'flow', 'cap'])

nextNodeIndex = list()
level = list()

ITERATION = 1
SOURCE = 0
DESTINATION = 0
MAXVAL = 1000000000

G = nx.DiGraph()
G_color = []
G_edgeLabel = []


def step_log(txt):
    if LOG_STEPS:
        print("STEP:", txt)


def G_DRAW(graph, title):
    G = nx.DiGraph()
    if GRAPH_RESIZE:
        fig = plt.figure(figsize=(GRAPH_SIZE, GRAPH_SIZE), facecolor="#F5F5F5")
    G_edgeLabel = {}
    G_color = []
    G_count = 1
    plt.title(title)
    for i in graph:
        for j in i:
            if title == "Final Graph":
                if j.flow > 0:
                    if j.flow == j.cap:
                        G.add_edge(G_count, j.nextNode + 1, color=EDGE_OVERLOADED, weight=2)
                    else:
                        G.add_edge(G_count, j.nextNode + 1, color=EDGE_DEFAULT, weight=1)
                    G_edgeLabel.update({(G_count, j.nextNode + 1): str(j.flow) + "/" + str(j.cap)})
            else:
                if j.flow >= 0:
                    if j.flow == j.cap:
                        G.add_edge(G_count, j.nextNode + 1, color=EDGE_OVERLOADED, weight=2)
                    else:
                        G.add_edge(G_count, j.nextNode + 1, color=EDGE_DEFAULT, weight=1)
                    G_edgeLabel.update({(G_count, j.nextNode + 1): str(j.flow) + "/" + str(j.cap)})
        G_count += 1

    for node in G:
        if node == SOURCE + 1:
            G_color.append(NODE_SOURCE)
        elif node == DESTINATION + 1:
            G_color.append(NODE_SINK)
        else:
            G_color.append(NODE_DEFAULT)

    pos = nx.circular_layout(G, scale=5)

    edges = G.edges()
    colors = list(nx.get_edge_attributes(G, 'color').values())
    weights = list(nx.get_edge_attributes(G, 'weight').values())
    for i in range(0, len(weights)):
        weights[i] *= GRAPH_SIZE * 0.15

    nx.draw(G, pos, edges=edges, alpha=1, node_color=G_color, with_labels=True, width=weights, edge_color=colors,
            node_size=GRAPH_SIZE * 150, font_size=15)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=G_edgeLabel, edge_sizes=GRAPH_SIZE * 50)
    plt.show()
    saveFileName = FILE_LOCATION_ROOT + FILE_LOCATION_GRAPHS + title + ".png"
    if SAVE_GRAPHS:
        fig.savefig(saveFileName)


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
    global ITERATION
    if currNode == destNode:
        return currMinFlow

    for nextNodeIndex[currNode] in range(nextNodeIndex[currNode], len(graph[currNode])):
        e = graph[currNode][nextNodeIndex[currNode]]

        if level[e.nextNode] == level[currNode] + 1 and e.flow < e.cap:
            nextFlow = min(currMinFlow, e.cap - e.flow)
            dfsVal = dfs(e.nextNode, destNode, nextFlow, graph)

            if dfsVal > 0:
                e.flow += dfsVal
                graph[e.nextNode][e.reverseIndex].flow -= dfsVal
                return dfsVal
    if DRAW_ITERATION_GRAPH:
        G_title = "Iteration #" + str(ITERATION)
        ITERATION += 1
        step_log("Drawing graph iteration...")
        G_DRAW(graph, G_title)
        step_log("Graph iteration drawing complete!")
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
step_log("Adding edges from excel file...")

# READING DATA FROM EXCEL FILE
wb = xlrd.open_workbook(FILE_LOCATION_ROOT + FILE_LOCATION_DATA)
sheet = wb.sheet_by_index(0)

numNodes = int(sheet.cell_value(0, 0))
numEdges = int(sheet.cell_value(0, 1))
for i in range(0, numNodes):
    level.append(0)
    nextNodeIndex.append(0)
for i in range(0, numNodes):
    graph.append(list())

for i in range(1, sheet.nrows):
    src = int(sheet.row_values(i)[0] - 1)
    dest = int(sheet.row_values(i)[1] - 1)
    weight = int(sheet.row_values(i)[2])
    addEdge(src, dest, weight, graph)

step_log("All edges added.")

SOURCE = int(sheet.cell_value(0, 2)) - 1
DESTINATION = int(sheet.cell_value(0, 3)) - 1

if DRAW_INITIAL_GRAPH:
    step_log("Drawing initial graph...")
    G_DRAW(graph, "Initial Graph")
    step_log("Initial graph drawing complete!")

print("Starting calculations from node", SOURCE + 1, "to node", DESTINATION + 1)
MAXFLOW = maxFlow(SOURCE, DESTINATION, graph)
step_log("Calculations done!")

print("Maximum Possible Flow: ", MAXFLOW)

if DRAW_FINAL_GRAPH:
    step_log("Drawing final graph...")
    G_DRAW(graph, "Final Graph")
    step_log("Final graph drawing complete!")
