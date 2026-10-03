# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def QFT(n):
    qubits = _global_qubits[:n]
    prog = pq.QProg()

    def qft_rotations(m):
        if m == 0:
            return
        m -= 1
        prog.insert(pq.H(qubits[m]))
        for qubit in range(m):
            angle = np.pi / (2 ** (m - qubit))
            prog.insert(pq.CP(qubits[qubit], qubits[m], angle))
        qft_rotations(m)

    def swap_registers(size):
        for qubit in range(size // 2):
            prog.insert(pq.SWAP(qubits[qubit], qubits[size - qubit - 1]))

    qft_rotations(n)
    swap_registers(n)
    return prog

machine.finalize()
