# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(50)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    q = qubits[:n]
    circuit = QCircuit()
    indices = [i for i, p in enumerate(pauli_string) if p != 'I']
    if not indices:
        return circuit
    for i in indices:
        p = pauli_string[i]
        if p == 'X':
            circuit << H(q[i])
        elif p == 'Y':
            circuit << RX(q[i], np.pi / 2)
    for j in range(len(indices) - 1):
        circuit << CNOT(q[indices[j]], q[indices[j + 1]])
    circuit << RZ(q[indices[-1]], 2 * time)
    for j in reversed(range(len(indices) - 1)):
        circuit << CNOT(q[indices[j]], q[indices[j + 1]])
    for i in reversed(indices):
        p = pauli_string[i]
        if p == 'X':
            circuit << H(q[i])
        elif p == 'Y':
            circuit << RX(q[i], -np.pi / 2)
    return circuit

machine.finalize()
