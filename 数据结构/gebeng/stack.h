#ifndef STACK_H
#define STACK_H
#pragma once
#include "graph.h"
typedef struct {
    int x, y, di, step;
}P;
typedef struct{
    P data[MAXSIZE * MAXSIZE];
    int top;
}SqStack;
void init_S(SqStack& S);
bool empty(SqStack S);
bool push(SqStack& S, P x);
bool pop(SqStack& S, P &x);
bool top(SqStack& S, P& x);
void print(SqStack S);
#endif // STACK_H
