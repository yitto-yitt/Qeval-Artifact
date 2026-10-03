# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import atexit

machine = CPUQVM()
machine.init_qvm()
MAX_QUBITS = 20
q_global = machine.qAlloc_many(MAX_QUBITS)

def QFT(n):
    q = q_global[:n]
    prog = QProg()

    def qft_rotations(prog, n):
        if n == 0:
            return
        n -= 1
        prog << H(q[n])
        for qubit in range(n):
            prog << CP(q[qubit], q[n], np.pi / 2 ** (n - qubit))
        qft_rotations(prog, n)

    def swap_registers(prog, n):
        for qubit in range(n // 2):
            prog << SWAP(q[qubit], q[n - qubit - 1])

    qft_rotations(prog, n)
    swap_registers(prog, n)
    return prog

atexit.register(machine.finalize)
