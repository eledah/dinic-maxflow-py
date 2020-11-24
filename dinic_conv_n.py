import math
import time
import xlrd
import networkx as nx
from queue import Queue
from random import random
import matplotlib.pyplot as plt
from recordtype import recordtype

# Configurations
LOG_STEPS = False

# Drawing Config
DRAW_INITIAL_GRAPH = True
DRAW_ITERATION_GRAPH = False
DRAW_FINAL_GRAPH = True
GRAPH_SIZE = 5
SAVE_GRAPHS = True

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
Edge = recordtype('Edge', ['nextNode', 'reverseIndex', 'flow', 'cap', 'i'])

nextNodeIndex = list()
level = list()
forwardGraph = list()

ITERATION = 1
MAXVAL = 1000000000


def step_log(txt):
    if LOG_STEPS:
        print("STEP:", txt)


def readExcel():
    # READING DATA FROM EXCEL FILE
    wb = xlrd.open_workbook(FILE_LOCATION_ROOT + FILE_LOCATION_DATA)
    sheet = wb.sheet_by_index(0)

    nodes = int(sheet.cell_value(0, 0))
    edges = int(sheet.cell_value(0, 1))
    for i in range(0, nodes):
        level.append(0)
        nextNodeIndex.append(0)
        graph.append(list())
        forwardGraph.append(list())

    for i in range(1, sheet.nrows):
        src = int(sheet.row_values(i)[0] - 1)
        dest = int(sheet.row_values(i)[1] - 1)
        weight = int(sheet.row_values(i)[2])
        addEdge(src, dest, weight, graph, i)

    src = int(sheet.cell_value(0, 2)) - 1
    dest = int(sheet.cell_value(0, 3)) - 1

    return nodes, edges, src, dest


def G_DRAW(graph, title):
    G = nx.MultiDiGraph()
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
                        G.add_edge(G_count, j.nextNode + 1, color=EDGE_OVERLOADED, weight=2,
                                   length=math.floor(random() * 4 + 1))
                    else:
                        G.add_edge(G_count, j.nextNode + 1, color=EDGE_DEFAULT, weight=1,
                                   length=math.floor(random() * 4 + 1))
                    G_edgeLabel.update({(G_count, j.nextNode + 1): str(j.flow) + "/" + str(j.cap)})
            else:
                if j.flow >= 0:
                    if j.flow == j.cap:
                        G.add_edge(G_count, j.nextNode + 1, color=EDGE_OVERLOADED, weight=2,
                                   length=math.floor(random() * 40 + 10))
                    else:
                        G.add_edge(G_count, j.nextNode + 1, color=EDGE_DEFAULT, weight=1,
                                   length=math.floor(random() * 40 + 10))
                    G_edgeLabel.update({(G_count, j.nextNode + 1): str(j.flow) + "/" + str(j.cap)})
        G_count += 1

    for node in G:
        if node == SOURCE + 1:
            G_color.append(NODE_SOURCE)
        elif node == DESTINATION + 1:
            G_color.append(NODE_SINK)
        else:
            G_color.append(NODE_DEFAULT)

    pos = nx.shell_layout(G, scale=5)

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


def addEdge(prevNode, nextNode, weight, graph, i):
    global forwardGraph
    forward = Edge(nextNode, len(graph[nextNode]), 0, weight, i)
    backward = Edge(prevNode, len(graph[prevNode]), 0, 0, i)

    graph[prevNode].append(forward)
    graph[nextNode].append(backward)
    forwardGraph[prevNode].append(forward)


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
                # print("SALAM", currNode + 1, e.nextNode + 1, e.reverseIndex + 1, e.flow, e.cap, dfsVal)
                # print(graph[e.nextNode][e.reverseIndex])
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
numNodes, numEdges, SOURCE, DESTINATION = readExcel()
step_log("All edges added.")

if DRAW_INITIAL_GRAPH:
    step_log("Drawing initial graph...")
    G_DRAW(forwardGraph, "Initial Graph")
    step_log("Initial graph drawing complete!")

print("Starting calculations from node", SOURCE + 1, "to node", DESTINATION + 1)
start_time = time.time()
MAXFLOW = maxFlow(SOURCE, DESTINATION, graph)
step_log("Calculations done!")
print("Calculation Runtime:", "--- %.3f seconds ---" % (time.time() - start_time))

print("Maximum Possible Flow:", MAXFLOW)

if DRAW_FINAL_GRAPH:
    step_log("Drawing final graph...")
    G_DRAW(graph, "Final Graph")
    step_log("Final graph drawing complete!")
