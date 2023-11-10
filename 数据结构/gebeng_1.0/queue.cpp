#include "queue.h"
void init_Q(SqQueue& Q)
{
	Q.front = Q.rear = 0;
}
bool empty(SqQueue Q)
{
	return Q.front == Q.rear;
}
bool append(SqQueue &Q, P1 x)
{
	if ((Q.rear + 1) % MAXSIZE == Q.front) return false;
	Q.data[Q.rear] = x;
	Q.rear = (Q.rear + 1) % MAXSIZE;
	return true;
}
bool popleft(SqQueue& Q, P1 &x)
{
	if (empty(Q)) return false;
	x = Q.data[Q.front];
	Q.front = (Q.front + 1) % MAXSIZE;
	return true;
}
void print(SqQueue Q)
{

	while (Q.front != Q.rear)
	{
		if ((Q.front + 1) % MAXSIZE != Q.rear)
			cout << "(" << Q.data[Q.front].x << "," << Q.data[Q.front].y << ")" << "->";
		else
			cout << "(" << Q.data[Q.front].x << "," << Q.data[Q.front].y << ")";
		Q.front = (Q.front + 1) % MAXSIZE;
	}
	puts("");
}