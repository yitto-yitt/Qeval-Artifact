# EVAL_META: task_id=65, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import *

def QFT(n):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    prog = QProg()

    def qft_rotations(prog, q, m):
        if m == 0:
            return
        m -= 1
        prog << H(q[m])
        for qubit in range(m):
            angle = pi / (2 ** (m - qubit))
            prog << CR(q[qubit], q[m], angle)
        qft_rotations(prog, q, m)

    def swap_registers(prog, q, n):
        for qubit in range(n // 2):
            prog << SWAP(q[qubit], q[n - qubit - 1])

    qft_rotations(prog, q, n)
    swap_registers(prog, q, n)
    return prog
