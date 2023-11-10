#include "graph.h"
#include "stack.h"
#include "queue.h"
// ①定义为全局变量，分配堆空间，更大，如果在main函数里会爆炸栈
Graph1 G1;
Graph2 G2;
SqStack S;
SqQueue Q;
int d[4][2] = { {0,1},{1,0},{0,-1},{-1,0} };
Point path[MAXSIZE * MAXSIZE], min_path[MAXSIZE * MAXSIZE];
int memo[MAXSIZE][MAXSIZE];
Point fa[MAXSIZE][MAXSIZE];
int memo1[MAXSIZE][MAXSIZE][5];
int idx, min_step = inf;
bool vis[MAXSIZE][MAXSIZE];
void init();
void dfs_stack(int s_x, int s_y, int e_x, int e_y);
void dfs_recursion(int x, int y, int step);
void bfs_queue(int s_x, int s_y, int e_x, int e_y);
void save_bfs(int x, int y,int step);
void judge();
int main()
{
	cout << "--------------Welcome to the problem of maze--------------" << '\n' << '\n';
	
	cout <<'\n' << "方 案 一 ：用 栈 实 现 的 非 递 归 D F S 算 法 : " << '\n' << '\n';
	init();
	dfs_stack(1, 1, G1.m, G1.n);
	judge();
	cout <<'\n' << "方 案 二 ：递 归 D F S 算 法 : " << '\n' << '\n';
	init();
	dfs_recursion(1, 1, 0);
	judge();
	
	cout << '\n' << "额 外 任 务 1 之 方 案 三 ：用 队 列 实 现 B F S 算 法 : " << '\n' << '\n';
	init();
	bfs_queue(1, 1, G1.m, G1.n);
	judge();

	cout << '\n' << "额 外 任 务 2 ：使 用 邻 接 表 存 储 迷 宫 " << '\n' << '\n';
	Create2(G2, G1);
	Print2(G2);
	return 0;
}



void init()
{
	for (int i = 0; i < MAXSIZE; i++) for (int j = 0; j < MAXSIZE; j++) 
	{
		memo[i][j] = 0x3f3f3f3f; vis[i][j] = 0; 
		for (int k = 0; k < 5; k++) memo1[i][j][k] = 0x3f3f3f3f;
	}
	idx = 0; min_step = inf;
	Create1(G1);
	Print1(G1);
	init_S(S);
	init_Q(Q);
}
void judge()
{
	if (min_step == inf) 
	{
		cout << "There's no path from (1,1) to (" << G1.m << "," << G1.n << ")" << '\n';
	}
	else
	{
		cout << "The minimum length of path is :" << min_step << '\n';
		cout << "(" << 1 << "," << 1 << ")" << "->";
		for (int i = 0; i < min_step - 1; i++)
		{
			cout << "(" << min_path[i].x << "," << min_path[i].y << ")" << "->";
		}
		cout << "(" << min_path[min_step - 1].x << "," << min_path[min_step - 1].y << ")" << '\n';
	}
}
void save_stack()
{
	for (int i = 0; i < min_step; i++) min_path[i] = { S.data[i + 1].x,S.data[i + 1].y };
}
void dfs_stack(int s_x, int s_y, int e_x, int e_y)
{
	bool find; int di;
	P start = { s_x,s_y,-1,0 };
	vis[s_x][s_y] = 1;
	push(S, start);
	for (int k = 0; k < 5; k++) memo1[1][1][k] = 0x3f3f3f3f;
	while (!empty(S))
	{
		P cur, tmp; top(S, cur); di = cur.di;
		if (cur.x == e_x && cur.y == e_y)
		{
			if (cur.step < min_step)
			{
				min_step = cur.step;
				save_stack();
			}
			vis[e_x][e_y] = 0;
			if (pop(S, cur))
			{
				top(S, cur);
				di = cur.di;
			}
			else break;
		}
		//记忆化搜索！
		if (memo1[cur.x][cur.y][cur.di + 1] > cur.step) memo1[cur.x][cur.y][cur.di + 1] = cur.step;
		else
		{
			if (pop(S, cur))
			{
				vis[cur.x][cur.y] = 0;
				top(S, cur);
				di = cur.di;
			}
			else break;
		}
		find = false;
		P ne;
		while (di < 4 && !find)
		{
			di++;
			if (di == 4) break;
			ne.x = cur.x + d[di][0]; ne.y = cur.y + d[di][1];
			if (ne.x >= 1 && ne.x <= G1.m && ne.y >= 1 && ne.y <= G1.n && vis[ne.x][ne.y] == 0 && G1.grid[ne.x][ne.y] == 0) find = true;
		}
		if (find)
		{
			pop(S, tmp);
			cur.di = di;
			push(S, cur);
			ne.di = -1;
			vis[ne.x][ne.y] = 1;
			ne.step = cur.step + 1;
			push(S, ne);
		}
		else
		{
			pop(S, cur);
			vis[cur.x][cur.y] = 0;
		}
	}
}
void save_recursion()
{
	for (int i = 0; i < min_step; i++) min_path[i] = path[i];
}
void dfs_recursion(int x, int y, int step)
{
	if (x == G1.m && y == G1.n)
	{
		if (step < min_step)
		{
			min_step = step;
			save_recursion();
		}
		return;
	}
	// ②记忆化搜索，使速度更快
	if (memo[x][y] > step) memo[x][y] = step;
	else                   return;
	for (int i = 0; i < 4; i++)
	{
		int new_x = x + d[i][0];
		int new_y = y + d[i][1];
		if (new_x >= 1 && new_x <= G1.m && new_y >= 1 && new_y <= G1.n)
		{
			if (!vis[new_x][new_y] && !G1.grid[new_x][new_y])
			{
				vis[new_x][new_y] = 1;
				path[idx] = { new_x,new_y };
				idx++;
				dfs_recursion(new_x, new_y, step + 1);
				// 恢复现场
				vis[new_x][new_y] = 0;
				idx--;
			}
		}
	}
	return;
}
void save_bfs(int x, int y,int step)
{
	if (x == 1 && y == 1) 
	{
		return;
	}
	save_bfs(fa[x][y].x, fa[x][y].y,step - 1);
	min_path[step - 1] = { x,y };

}
void bfs_queue(int s_x,int s_y,int e_x,int e_y)
{
	P1 start = { s_x,s_y,0 };
	append(Q, start);
	while (!empty(Q))
	{
		P1 cur; popleft(Q, cur);
		if (cur.x == e_x && cur.y == e_y)
		{
			save_bfs(e_x, e_y,cur.step);
			min_step = cur.step;
			return;
		}
		for (int i = 0; i < 4; i++)
		{
			P1 ne; ne.x = cur.x + d[i][0]; ne.y = cur.y + d[i][1]; ne.step = cur.step + 1;
			if (ne.x >= 1 && ne.x <= G1.m && ne.y >= 1 && ne.y <= G1.n && vis[ne.x][ne.y] == 0 && G1.grid[ne.x][ne.y] == 0)
			{
				append(Q, ne);
				vis[ne.x][ne.y] = 1;
				fa[ne.x][ne.y] = { cur.x,cur.y};
			}
		}
	}
}