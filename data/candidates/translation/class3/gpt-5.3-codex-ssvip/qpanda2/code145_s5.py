# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def qft_inverse(n):
    qubits = _global_qubits[:n]
    prog = pq.QProg()
    for i in range(n // 2):
        prog << pq.SWAP(qubits[i], qubits[n - i - 1])
    for j in range(n):
        for k in range(j):
            angle = -3.141592653589793 / (2 ** (j - k))
            prog << pq.CR(qubits[j], qubits[k], angle)
        prog << pq.H(qubits[j])
    return prog

machine.finalize()
