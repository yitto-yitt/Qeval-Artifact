# EVAL_META: task_id=145, framework=qpanda2, class=3
import atexit
from math import pi
from operator import index
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)


def qft_inverse(n):
    n = index(n)
    if n < 0:
        raise ValueError("The number of qubits must be nonnegative.")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    for j in range(n - 1, -1, -1):
        circuit << pq.H(qubits[j])
        for k in range(j - 1, -1, -1):
            circuit << pq.U1(
                qubits[k], pi / (2 ** (j - k))
            ).control([qubits[j]])

    for j in range(n // 2):
        circuit << pq.SWAP(qubits[j], qubits[n - j - 1])

    return circuit.dagger()
