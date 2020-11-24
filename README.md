# dinic-maxflow-py
![](https://img.shields.io/badge/category-GraphTheory-informational?style=flat&logoColor=white&color=7E57C2) ![](https://img.shields.io/badge/category-Transportation-informational?style=flat&logoColor=white&color=F57C00) ![](https://img.shields.io/badge/code-python3-informational?style=flat&logoColor=white&color=42A5F5) ![](https://img.shields.io/badge/code-c++-informational?style=flat&logo=c++&logoColor=white&color=EC407A)


Maximum flow calculation for any graph network using Dinic's algorithm.

<a href="https://en.wikipedia.org/wiki/Dinic%27s_algorithm">Wikipedia Article</a>



## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Contact](#contact)

## General info
The goal of this project to is calculate the maximum amount of available flow between any two points (the source and the sink) in a given graph network.

## Screenshots
The two images below show both the initial and the solved graphs. The red nodes are the sources, green nodes are the sinks and the blue nodes are the ones that are inbetween. The red edges in the final graph indicated the edges that are passing the full possible flow.
 
<img src="https://github.com/eledah/tpmaxflow-py/blob/main/output/visual/Initial%20Graph.png" width="300"> <img src="https://github.com/eledah/tpmaxflow-py/blob/main/output/visual/Final%20Graph.png" width="300">

## Setup
### Python ver.
Set _FILE_LOCATION_ROOT_ under _#File Config_ to the where the master folder is located. Then change _FILE_LOCATION_DATA_ to choose the dataset. 

In order to add the dataset of your own, do as following:

1- Create an Excel file in ./root/data/

2- The first line of the first sheet should be like this: 

| Total Number of Edges  | Total Number of Nodes | Source Node Number | Sink Node Number |

3- The next lines will contain the edges' data. Each row is dedicated to the source node, destination node and the edge weight.

|       Source Node      |    Destination Node   |     Edge Weight    |

4- Save the file, alter the configurations as desired and run the code.

### C++ ver.
Inputting data must be in the following order:

[Total Nodes] [Total Edges]

[Source Node] [Destination Node] [Edge Weight]

[Source Node] [Destination Node] [Edge Weight]

And so on until all the edges are given to the program.

## Contact
[@eledah](https://www.t.me/eledah)
