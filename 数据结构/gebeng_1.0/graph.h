#pragma once
#pragma once
#include <iostream>
using namespace std;
const int inf = 0x3f3f3f3f;
const int MAXSIZE = 105;
// �ڽӾ���洢�����Թ���0����ͨ·��1�����ϰ���
typedef struct
{
    int grid[MAXSIZE][MAXSIZE];
    int m, n;
}Graph1;
// ����洢���·���Ľṹ�����飡
typedef struct
{
    //��¼·���ĵ������
    int x, y;
}Point;
typedef struct ArcNode 
{
    Point adjvex;
    struct ArcNode* nextarc;
}ArcNode;
typedef struct
{
    ArcNode* firstarc;
}VNode,AdjList[MAXSIZE][MAXSIZE];
typedef struct
{
    AdjList vertices;
    int m,n, arcnum;
}Graph2;
void Create1(Graph1& G);
void Print1(Graph1& G);
void Create2(Graph2& G,Graph1 tmp);
void Print2(Graph2& G);