# EVAL_META: task_id=145, framework=qpanda2, class=3
import math
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
try:
    machine.set_configure(64, 64)
except Exception:
    pass
machine.init_qvm()
qubits = machine.qAlloc_many(64)

def qft_inverse(n):
    if n > len(qubits):
        raise ValueError("n exceeds globally allocated qubits")

    circuit = pq.QCircuit()

    for i in range(n // 2):
        circuit.insert(pq.SWAP(qubits[i], qubits[n - i - 1]))

    for j in range(n):
        for k in range(j):
            circuit.insert(pq.CR(qubits[k], qubits[j], -math.pi / (1 << (j - k))))
        circuit.insert(pq.H(qubits[j]))

    return circuit

atexit.register(machine.finalize)
