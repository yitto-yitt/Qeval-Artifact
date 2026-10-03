# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.init_qvm()

def QFT(n):
    q = machine.qAlloc_many(n)
    prog = QProg()

    def qft_rotations(m, q, num):
        if num == 0:
            return
        num -= 1
        m << H(q[num])
        for qubit in range(num):
            m << CP(q[qubit], q[num], pi / (2 ** (num - qubit)))
        qft_rotations(m, q, num)

    def swap_registers(m, q, num):
        for qubit in range(num // 2):
            a = q[qubit]
            b = q[num - qubit - 1]
            m << CNOT(a, b) << CNOT(b, a) << CNOT(a, b)

    qft_rotations(prog, q, n)
    swap_registers(prog, q, n)
    return prog

machine.finalize()
