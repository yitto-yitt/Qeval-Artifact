# EVAL_META: task_id=145, framework=qpanda2, class=3
import math
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(32)

def qft_inverse(n):
    qubits = q[:n]
    circuit = pq.QCircuit()

    for i in range(n // 2):
        circuit << pq.SWAP(qubits[i], qubits[n - i - 1])

    for j in range(n):
        for m in range(j):
            circuit << pq.CR(qubits[m], qubits[j], -math.pi / (2 ** (j - m)))
        circuit << pq.H(qubits[j])

    return circuit

atexit.register(machine.finalize)
