# EVAL_META: task_id=145, framework=qpanda2, class=3
import atexit
import math
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(29)
atexit.register(machine.finalize)


def qft_inverse(n):
    n = operator.index(n)
    if not 0 <= n <= len(qubits):
        raise ValueError("n must be between 0 and 29.")

    circuit = pq.QCircuit()

    for j in range(n // 2):
        circuit << pq.SWAP(qubits[j], qubits[n - 1 - j])

    for j in range(n):
        for k in range(j):
            angle = -math.pi / (2 ** (j - k))
            circuit << pq.U1(qubits[k], angle).control([qubits[j]])
        circuit << pq.H(qubits[j])

    return circuit
