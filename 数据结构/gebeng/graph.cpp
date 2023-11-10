#include "graph.h"
#include<ctime>
#include<random>
// 这里还要再这一个，且不能与widget.cpp中的重名，会报错！
int d3[4][2] = { {0,1},{1,0},{0,-1},{-1,0} };
void Create1(Graph1& G)
{
    default_random_engine e;
    // 生成1的概率为0.3，则生成0的概率为0.7
    bernoulli_distribution u(0.3);
    cout << "Please input the row and col of maze:";
    cin >> G.m >> G.n;
    for (int i = 1; i <= G.m; i++)
    {
        for (int j = 1; j <= G.n; j++)
        {
            G.grid[i][j] = u(e);
        }
    }
    // 保证起点与终点无障碍
    G.grid[1][1] = G.grid[G.m][G.n] = 0;
}
void Print1(Graph1& G)
{
    puts("----------------------------------------------------------------------");
    for (int i = 1; i <= G.m; i++)
    {
        for (int j = 1; j <= G.n; j++)
        {
            cout << G.grid[i][j] << " ";
        }
        puts("");
    }
    puts("----------------------------------------------------------------------");
}
void Create2(Graph2& G,Graph1 tmp)
{
    G.arcnum = 0;
    G.m = tmp.m;G.n =  tmp.n;
    default_random_engine e;
    // 生成1的概率为0.3，则生成0的概率为0.7
    bernoulli_distribution u(0.3);
    for (int i = 1; i <= G.m; i++)
    {
        for (int j = 1; j <= G.n; j++)
        {
            Point ne;
            for (int k = 0; k < 4; k++)
            {
                ne.x = i + d3[k][0], ne.y = j + d3[k][1];
                // cur 与 ne 之 间 有 边；
                if (ne.x >= 1 && ne.x <= tmp.m && ne.y >= 1 && ne.y <= tmp.n)
                {
                    if (tmp.grid[ne.x][ne.y] == 0)
                    {
                        G.arcnum += 1;
                        ArcNode* p = new ArcNode;
                        p->adjvex = ne;
                        p->nextarc = G.vertices[i][j].firstarc;
                        G.vertices[i][j].firstarc = p;
                    }
                }
            }
        }
    }
}
void Print2(Graph2& G)
{
    for (int i = 1; i <= G.m; i++)
    {
        for (int j = 1; j <= G.n; j++)
        {
            ArcNode* p = G.vertices[i][j].firstarc;
            cout << "(" << i << "," << j<< "):";
            while (p)
            {
                if(!p->nextarc)
                    cout << "(" << p->adjvex.x << "," << p->adjvex.y << ")";
                else
                    cout << "(" << p->adjvex.x << "," << p->adjvex.y << ")->";
                p = p->nextarc;
            }
            puts("");
        }

    }
}
