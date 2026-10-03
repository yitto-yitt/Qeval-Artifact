# EVAL_META: task_id=145, framework=qpanda2, class=3
import atexit
import math
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)

def qft_inverse(n):
    n = operator.index(n)
    if n < 0:
        raise ValueError("The number of qubits must be nonnegative.")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    for j in reversed(range(n)):
        circuit << pq.H(qubits[j])
        for k in reversed(range(j)):
            circuit << pq.CR(
                qubits[j], qubits[k], math.pi / (2 ** (j - k))
            )

    for j in range(n // 2):
        circuit << pq.SWAP(qubits[j], qubits[n - j - 1])

    return circuit.dagger()

atexit.register(lambda: machine.finalize())
