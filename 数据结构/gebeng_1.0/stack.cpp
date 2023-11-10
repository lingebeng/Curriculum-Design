#include "stack.h"
void init_S(SqStack& S)
{
	S.top = -1;
}
bool empty(SqStack S)
{
	return S.top == -1;
}
bool push(SqStack& S, P x)
{
	if (S.top == MAXSIZE * MAXSIZE - 1) return false;
	S.data[++S.top] = x;
	return true;
}
bool pop(SqStack& S, P& x)
{
	if (empty(S)) return false;
	x = S.data[S.top--];
	return true;
}
bool top(SqStack& S, P& x)
{
	if (empty(S)) return false;
	x = S.data[S.top];
	return true;
}
void print(SqStack S)
{
	for (int i = 0; i <= S.top - 1; i++)
	{
		cout << "(" << S.data[i].x << "," << S.data[i].y << ")" << "->";
	}
	cout << "(" << S.data[S.top].x << "," << S.data[S.top].y << ')' << '\n';
}