# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
from numpy import pi

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def QFT(n):
    qubits = _global_qubits[:n]
    prog = pq.QProg()

    def qft_rotations(k):
        if k == 0:
            return
        k -= 1
        prog.insert(pq.H(qubits[k]))
        for qubit in range(k):
            angle = pi / (2 ** (k - qubit))
            prog.insert(pq.CU(1.0, 0.0, 0.0, angle, qubits[qubit], qubits[k]))
        qft_rotations(k)

    qft_rotations(n)

    for i in range(n // 2):
        prog.insert(pq.SWAP(qubits[i], qubits[n - i - 1]))

    machine.directly_run(prog)
    machine.finalize()
    return prog
