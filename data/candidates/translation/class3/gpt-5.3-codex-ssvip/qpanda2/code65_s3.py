# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def QFT(n):
    qubits = _global_qubits[:n]
    prog = pq.QProg()

    def qft_rotations(qprog, qs, m):
        if m == 0:
            return
        m -= 1
        qprog << pq.H(qs[m])
        for qubit in range(m):
            angle = np.pi / (2 ** (m - qubit))
            qprog << pq.CU(1.0, 0.0, 0.0, angle, qs[qubit], qs[m])
        qft_rotations(qprog, qs, m)

    def swap_registers(qprog, qs, m):
        for qubit in range(m // 2):
            qprog << pq.SWAP(qs[qubit], qs[m - qubit - 1])

    qft_rotations(prog, qubits, n)
    swap_registers(prog, qubits, n)
    machine.directly_run(prog)
    machine.finalize()
    return prog
