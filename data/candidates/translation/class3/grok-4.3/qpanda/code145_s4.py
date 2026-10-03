# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import *
def qft_inverse(n):
    qprog = QProg()
    q = qAlloc_many(n)
    for i in range(n//2):
        qprog << SWAP(q[i], q[n-1-i])
    for i in range(n):
        for j in range(i):
            qprog << CR(q[j], q[i], -2*3.141592653589793/2**(i-j+1))
    for i in range(n):
        qprog << H(q[i])
    return qprog
