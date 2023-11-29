#include "widget.h"
#include "ui_widget.h"
#include "graph.h"
#include "stack.h"
#include "queue.h"
#include<stdlib.h>
#include<time.h>
#include<QPen>
#include<QBrush>
#include<QTimer>
#include<QPixmap>
#include<QString>
#include<QMessageBox>
#include<QIcon>
#include<cmath>
#include <cstdlib>
#include <ctime>
#include<fstream>
#include<stdlib.h>
// ①定义为全局变量，分配堆空间，更大，如果在main函数里会爆炸栈
Graph1 G1;
Graph2 G2;
SqStack S;
SqQueue Q;
// 特意设置保证三种方法的路径不一样！
int d[4][2] = { {0,1},{1,0},{0,-1},{-1,0} };
int d1[4][2] = { {1,0},{0,1},{-1,0},{0,-1} };
int d2[4][2] = { {-1,0},{0,-1},{0,1},{1,0} };
Point path[MAXSIZE * MAXSIZE], min_path[MAXSIZE * MAXSIZE];
int memo[MAXSIZE][MAXSIZE];
Point fa[MAXSIZE][MAXSIZE];
int memo1[MAXSIZE][MAXSIZE][5];
int idx, min_step = inf;
bool vis[MAXSIZE][MAXSIZE];
bool path_record[MAXSIZE][MAXSIZE];
void init();

void dfs_stack(int s_x, int s_y, int e_x, int e_y);
void dfs_recursion(int x, int y, int step);
void bfs_queue(int s_x, int s_y, int e_x, int e_y);

void save_stack();
void save_recursion();
void save_bfs(int x, int y,int step);

int row = 10,col = 10;
double random = 0.2,t = 0.00;

int seed;
Widget::Widget(QWidget *parent): QWidget(parent), ui(new Ui::Widget)
{
    ui->setupUi(this);
    // 显示图标
    this->setWindowIcon(QIcon(":/image/love.jpg"));
    // 确认按钮
    connect(ui->ensure1_btn,&QPushButton::clicked,[&](){
        srand((unsigned int)time(NULL));
        seed = rand() % 100 + 1;
        row = ui->row_spin->value();
        col = ui->col_spin->value();
        random = ui->random_spin->value();
        init();
        this->update();
    });
    // dfs_stack按钮
    connect(ui->dfs_stack_btn,&QPushButton::clicked,[&](){
        init();
        clock_t start, finish;
        start = clock();
        dfs_stack(1, 1, G1.m, G1.n);
        finish = clock();
        t = (double)finish - start;
        if(min_step == inf) {
            ui->min_step->setText("inf");
            ui->run_time->setText("inf");
            QMessageBox message;
            message.critical(this, tr("提示"),  tr("找不到最短路径"), QMessageBox::Discard);
            QIcon *icon = new QIcon(":/image/favicon.ico");
            message.setWindowIcon(*icon);
        }
        else{
            QVariant v(t);
            QString s = v.toString();
            ui->run_time->setText(s);
            QVariant v1(min_step);
            QString s1 = v1.toString();
            ui->min_step->setText(s1);
        }

        this->update();
    });
    // dfs_recursion按钮
    connect(ui->dfs_recursion_btn,&QPushButton::clicked,[&](){
        init();
        clock_t start, finish;
        start = clock();
        dfs_recursion(1, 1, 0);
        finish = clock();
        t = (double)finish - start;
        if(min_step == inf) {
            ui->min_step->setText("inf");
            ui->run_time->setText("inf");
            QMessageBox message;
            message.critical(this, tr("提示"),  tr("找不到最短路径"), QMessageBox::Discard);
            QIcon *icon = new QIcon(":/image/favicon.ico");
            message.setWindowIcon(*icon);
        }
        else{
            QVariant v(t);
            QString s = v.toString();
            ui->run_time->setText(s);
            QVariant v1(min_step);
            QString s1 = v1.toString();
            ui->min_step->setText(s1);
        }
        this->update();
    });
    // bfs_queue按钮
    connect(ui->bfs_queue_btn,&QPushButton::clicked,[&](){
        init();
        clock_t start, finish;
        start = clock();
        bfs_queue(1, 1, G1.m, G1.n);
        finish = clock();
        t = (double)finish - start;
        if(min_step == inf) {
            ui->min_step->setText("inf");
            ui->run_time->setText("inf");
            QMessageBox message;
            message.critical(this, tr("提示"),  tr("找不到最短路径"), QMessageBox::Discard);
            QIcon *icon = new QIcon(":/image/favicon.ico");
            message.setWindowIcon(*icon);
        }
        else{
            QVariant v(t);
            QString s = v.toString();
            ui->run_time->setText(s);
            QVariant v1(min_step);
            QString s1 = v1.toString();
            ui->min_step->setText(s1);
        }
        this->update();
    });
}
// 求两个浮点数的最小值函数
double mi(double a,double b)
{
    if((a - b) <= 1e-6)
        return a;
    else
        return b;
}
Widget::~Widget()
{
    delete ui;
}

void Widget::paintEvent(QPaintEvent *event)
{

    QPainter painter(this);
    QPen pen;
    // 设置颜色，字宽
    pen.setColor(QColor(0,0,205));
    pen.setWidth(1);
    pen.setStyle(Qt::DotLine);
    painter.setPen(pen);
    // 这里处理的方格的相对大小
    double M = mi(600 / row,600/col);
    //    default_random_engine e(seed);
    mt19937 e(seed);
    //生成1的概率为random，则生成0的概率为1 - random
    bernoulli_distribution u(random);
    G1.m = row;G1.n = col;
    for (int i = 1; i <= G1.m; i++)
    {
        for (int j = 1; j <= G1.n; j++)
        {
            G1.grid[i][j] = u(e);
        }
    }
    // 保证起点与终点无障碍！
    G1.grid[1][1] = G1.grid[G1.m][G1.n] = 0;
    // 画迷宫！
    for(int i = 0;i < row;i++)
    {
        for(int j = 0;j < col;j++)
        {
            if(G1.grid[i + 1][j + 1] <= 0)
            {
                painter.drawPixmap(j * M,i * M,M,M,QPixmap(":/image/true.jpg"));
            }
            else{
                painter.drawPixmap(j * M,i * M,M,M,QPixmap(":/image/false.jpg"));
            }
        }
    }
    // 在(1,1)画皮卡丘，（m,n）画精灵球
    painter.drawPixmap((col - 1) * M,(row-1) * M,M,M,QPixmap(":/image/finish.jpg"));
    painter.drawPixmap(0,0,M,M,QPixmap(":/image/love.jpg"));

    path_record[1][1] = 1;
    // 这里画得是最短路，只有当min_path里存得有最短路的坐标时才会显示，初始化为(0,0)
    for(int i = 0;i <= G1.m * G1.n;i++)
    {
        if(min_path[i].x != 0 && min_path[i].y != 0)
        {
            painter.drawPixmap((min_path[i].y - 1) * M,(min_path[i].x - 1) * M,M,M,QPixmap(":/image/love.jpg"));
        }
    }
    // 画蓝色虚线，显得更有层次感！
    for(int i = 0;i <= row;i++)
    {
        painter.drawLine(QPoint(0,i * M),QPoint(M * col,i * M));
    }
    for(int j = 0;j <= col;j++)
    {
        painter.drawLine(QPoint(j * M,0),QPoint(j * M,M * row));
    }

}
// 显示邻接矩阵
void Widget::on_adj_matrix_btn_clicked()
{
    // 写入1.txt文件
    ofstream ofile("1.txt");
    ofile << G1.m << " " << G1.n << "\n";
    for(int i = 1;i <= G1.m;i++)
    {
        for(int j = 1;j <= G1.n;j++)
        {
            ofile << G1.grid[i][j] << " ";
        }
        ofile <<'\n';
    }
    ofile.close();
    //使用系统调用记事本自动弹出1.txt文件
    system("notepad.exe 1.txt");
}
// 显示邻接表
void Widget::on_adj_list_btn_clicked()
{
    Create2(G2,G1);
    // 写入2.txt文件
    ofstream ofile("2.txt");
    ofile << G2.m << " " << G2.n << " " << G2.m * G2.n <<'\n';
    for (int i = 1; i <= G2.m; i++)
    {
        for (int j = 1; j <= G2.n; j++)
        {
            ArcNode* p = G2.vertices[i][j].firstarc;
            ofile << "(" << i   << ","  << j  << "):";
            while (p)
            {
                if(!p->nextarc)
                    ofile << "("  << p->adjvex.x  << ","  << p->adjvex.y <<")";
                else
                    ofile << "("  << p->adjvex.x  << ","  << p->adjvex.y <<")->";
                p = p->nextarc;
            }
            ofile<<'\n';
        }
    }
    ofile.close();
    //使用系统调用记事本自动弹出2.txt文件
    system("notepad.exe 2.txt");
}
// 显示最短路
void Widget::on_min_path_btn_clicked()
{
    // 写入3.txt文件
    ofstream ofile("3.txt");
    if (min_step == inf)
    {
        ofile << "There's no path from (1,1) to (" << G1.m << "," << G1.n << ")" << '\n';
    }
    else
    {
        int cnt = 0;
        ofile << "The minimum length of path is :" << min_step << '\n';
        ofile << "The execute time of algorithm is :" << t << "ms" << '\n';
        ofile << "(" << 1 << "," << 1 << ")" << "->";
        cnt++;
        for (int i = 0; i < min_step - 1; i++)
        {
            if(cnt % 10 == 0)
            {
                ofile << "(" << min_path[i].x << "," << min_path[i].y << ")" << "->\n";
            }
            else
            {
                ofile << "(" << min_path[i].x << "," << min_path[i].y << ")" << "->";
            }
            cnt ++;
            path_record[min_path[i].x][min_path[i].y] = 1;
        }
        ofile << "(" << min_path[min_step - 1].x << "," << min_path[min_step - 1].y << ")" << '\n';
        path_record[min_path[min_step - 1].x][min_path[min_step - 1].y] = 1;
    }
    for(int i = 1;i <= G1.m;i++)
    {
        for(int j = 1;j <= G1.n;j++)
        {
            if(path_record[i][j] == 1)  ofile<<"o ";
            else if(G1.grid[i][j] == 1) ofile<<"x ";
            else                        ofile<<"- ";
            path_record[i][j] = 0;//恢复为0，以便下一次记录！
        }
        ofile <<'\n';
    }
    ofile.close();
    //使用系统调用记事本自动弹出3.txt文件
    system("notepad.exe 3.txt");
}
// 初始化函数，初始化一些变量【记忆化数组、最短路存储数组，栈，队列，最短路长度等等】
void init()
{
    for (int i = 0; i < MAXSIZE; i++)
        for (int j = 0; j < MAXSIZE; j++)
        {
            memo[i][j] = 0x3f3f3f3f; vis[i][j] = 0;
            for (int k = 0; k < 5; k++) memo1[i][j][k] = 0x3f3f3f3f;
        }
    for(int i = 0;i <MAXSIZE * MAXSIZE;i++)
    {
        min_path[i].x = 0;min_path[i].y = 0;
    }
    idx = 0; min_step = inf;
    init_S(S);
    init_Q(Q);
}
// 将栈中存的最短路保存到min_step中，便于统一管理与控制！
void save_stack()
{
    for (int i = 0; i < min_step; i++) min_path[i] = { S.data[i + 1].x,S.data[i + 1].y };
}
void dfs_stack(int s_x, int s_y, int e_x, int e_y)
{
    // find标志【true表示找到了可以从当前节点扩展的节点】
    // di表示方向变量，初始化为-1，0、1、2、3，代表四个方向！
    bool find; int di;
    // 起点为(s_x,s_y),初始化方向为-1，并附带step信息【表示到达当前点，已经走过的步数，初始化为0】
    P start = { s_x,s_y,-1,0 };
    // vis数组标记(s_x,s_y),已经走过了，不可重复走！
    vis[s_x][s_y] = 1;
    // 将初始节点压入栈中！
    push(S, start);
    //    for (int k = 0; k < 5; k++) memo1[1][1][k] = 0x3f3f3f3f;

    //下面就是dfs的主体了！
    while (!empty(S))
    {
        // 设置cur表示当前坐标，并将栈顶元素赋给cur
        // tmp临时变量，di表示方向
        P cur, tmp; top(S, cur); di = cur.di;
        // 如果弹出的点恰好是终点，那说明找到了这一条路径！【注意只是找到了，并非最短】
        if (cur.x == e_x && cur.y == e_y)
        {
            // 这里维护的就是每一次找到的最短路径，所有路径都遍历完后，就是最终的最短路！
            if (cur.step < min_step)
            {
                min_step = cur.step;
                save_stack();
            }
            // 将终点标记为可访问，供下一条路径访问！
            vis[e_x][e_y] = 0;
            // 弹出栈顶元素，并将弹出后的栈顶元素付给cur
            if (pop(S, cur))
            {
                top(S, cur);
                di = cur.di;
            }
            else break;
        }
        // 记忆化搜索！
        // 如果当前方向之前已经走过，并且比现在走的最短路径长度短，那就更新记忆化数组!
//        cout <<"------" << memo1[cur.x][cur.y][cur.di + 1] << "------"<< cur.step << endl;
        if (memo1[cur.x][cur.y][cur.di + 1] > cur.step) memo1[cur.x][cur.y][cur.di + 1] = cur.step;
        // 否则就跳过当前点，直接弹出，dfs下一个点！
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
        // 初始化find为false，定义从cur节点找到的下一个节点
        find = false;
        P ne;
        // 上下左右四个方向，选取能扩展的第一个点，作为ne
        while (di < 4 && !find)
        {
            // 这里会更新cur的方向变量！
            di++;
            if (di == 4) break;
            ne.x = cur.x + d[di][0]; ne.y = cur.y + d[di][1];
            if (ne.x >= 1 && ne.x <= G1.m && ne.y >= 1 && ne.y <= G1.n && vis[ne.x][ne.y] == 0 && G1.grid[ne.x][ne.y] == 0) find = true;
        }
        //如果找到了
        if (find)
        {
            // 先弹出栈顶元素给tmp
            pop(S, tmp);
            // 再更新cur的方向
            cur.di = di;
            // 再将更新后cur放进栈中，这部操作主要是为了更新方向，当然也可以用&类型，这里就用原始的方法！
            push(S, cur);
            // 初始化新点的方向！
            ne.di = -1;
            // 更新标记数组为已访问！
            vis[ne.x][ne.y] = 1;
            // 更新ne.step，步数为cur加一！
            ne.step = cur.step + 1;
            // 再压入栈中
            push(S, ne);
            // 其实递归函数的调用也就是一个个函数栈，不断弹出压进的过程！
        }
        // 如果找不到，我们就将cur弹出，并标记为未访问
        else
        {
            pop(S, cur);
            vis[cur.x][cur.y] = 0;
        }
    }
}
// 保存由递归的dfs生成的最短路径！
void save_recursion()
{
    for (int i = 0; i < min_step; i++) min_path[i] = path[i];
}
void dfs_recursion(int x, int y, int step)
{
    // 如果找到一条路径
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
    // 上下左右四个方向
    for (int i = 0; i < 4; i++)
    {
        int new_x = x + d1[i][0];
        int new_y = y + d1[i][1];
        // 判断是否越界
        if (new_x >= 1 && new_x <= G1.m && new_y >= 1 && new_y <= G1.n)
        {
            // 判断是否访问过或者有障碍！
            if (!vis[new_x][new_y] && !G1.grid[new_x][new_y])
            {
                vis[new_x][new_y] = 1;
                path[idx] = { new_x,new_y };
                // idx是关键，用来保存最短路的！
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
// 保存bfs算法得到的最短路，回溯到（1，1）起点后，开始不断保存！
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
    // 初始节点入队！
    P1 start = { s_x,s_y,0 };
    append(Q, start);
    // 直到队列为空，或找到最短路！
    while (!empty(Q))
    {
        P1 cur; popleft(Q, cur);
        // 找到路径即是最短路！
        if (cur.x == e_x && cur.y == e_y)
        {
            save_bfs(e_x, e_y,cur.step);
            min_step = cur.step;
            return;
        }
        for (int i = 0; i < 4; i++)
        {
            P1 ne; ne.x = cur.x + d2[i][0]; ne.y = cur.y + d2[i][1]; ne.step = cur.step + 1;
            if (ne.x >= 1 && ne.x <= G1.m && ne.y >= 1 && ne.y <= G1.n && vis[ne.x][ne.y] == 0 && G1.grid[ne.x][ne.y] == 0)
            {
                append(Q, ne);
                // 标记为已访问，确保不会重复进入队列！
                vis[ne.x][ne.y] = 1;
                // fa数组是关键，表示fa[x][y]表示的是转移到(x,y)的上一个点！
                fa[ne.x][ne.y] = { cur.x,cur.y};
            }
        }
    }
}







