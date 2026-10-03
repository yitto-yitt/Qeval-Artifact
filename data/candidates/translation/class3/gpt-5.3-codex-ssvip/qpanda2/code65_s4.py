# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
from numpy import pi

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def QFT(n):
    qubits = _global_qubits[:n]
    prog = pq.QProg()

    def qft_rotations(prog_obj, qlist, m):
        if m == 0:
            return
        m -= 1
        prog_obj << pq.H(qlist[m])
        for qubit in range(m):
            angle = pi / (2 ** (m - qubit))
            prog_obj << pq.CP(qlist[qubit], qlist[m], angle)
        qft_rotations(prog_obj, qlist, m)

    def swap_registers(prog_obj, qlist, m):
        for qubit in range(m // 2):
            prog_obj << pq.SWAP(qlist[qubit], qlist[m - qubit - 1])

    qft_rotations(prog, qubits, n)
    swap_registers(prog, qubits, n)
    return prog

machine.finalize()
