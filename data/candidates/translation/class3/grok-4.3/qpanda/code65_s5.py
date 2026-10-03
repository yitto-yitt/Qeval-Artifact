# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
from numpy import pi

def QFT(n):
    prog = QProg()
    q = qAlloc_many(n)
    def swap_registers(prog, q, n):
        for i in range(n//2):
            prog << SWAP(q[i], q[n-i-1])
        return prog
    def qft_rotations(prog, q, n):
        if n == 0:
            return prog
        n -= 1
        prog << H(q[n])
        for qubit in range(n):
            prog << CR(pi/2**(n-qubit), q[qubit], q[n])
        qft_rotations(prog, q, n)
        return prog
    qft_rotations(prog, q, n)
    swap_registers(prog, q, n)
    return prog
