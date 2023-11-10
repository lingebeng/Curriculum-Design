#ifndef QUEUE_H
#define QUEUE_H
#include "graph.h"
typedef struct
{
    int x, y, step;
}P1;
typedef struct {
    P1 data[MAXSIZE];
    int front, rear;
}SqQueue;
void init_Q(SqQueue& Q);
bool empty(SqQueue Q);
bool append(SqQueue& Q, P1 x);
bool popleft(SqQueue& Q, P1& x);
void print(SqQueue Q);

#endif // QUEUE_H
