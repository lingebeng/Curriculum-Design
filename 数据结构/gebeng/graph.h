#ifndef GRAPH_H
#define GRAPH_H
#pragma once
#include <iostream>
using namespace std;
const int inf = 0x3f3f3f3f;
const int MAXSIZE = 105;
// 邻接矩阵存储整个迷宫，0代表通路，1代表障碍！
typedef struct
{
    int grid[MAXSIZE][MAXSIZE];
    int m, n;
}Graph1;
// 定义存储最短路径的结构体数组！
typedef struct
{
    //记录路径的点的坐标
    int x, y;
}Point;
// 边节点
typedef struct ArcNode
{
    Point adjvex;
    struct ArcNode* nextarc;
}ArcNode;
// 头节点
typedef struct
{
    ArcNode* firstarc;
}AdjList[MAXSIZE][MAXSIZE];
typedef struct
{
    AdjList vertices;
    int m,n, arcnum;
}Graph2;
// 邻接矩阵建图
void Create1(Graph1& G);
void Print1(Graph1& G);
// 邻接表建图
void Create2(Graph2& G,Graph1 tmp);
void Print2(Graph2& G);
#endif // GRAPH_H
