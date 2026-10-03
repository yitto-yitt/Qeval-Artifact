# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init()
MAX_QUBITS = 100
qubits = qAlloc_many(MAX_QUBITS)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    pauli = pauli_string[::-1]
    q = qubits[:n]
    circuit = QCircuit()
    non_identity = [i for i, p in enumerate(pauli) if p != 'I']

    for i, p in enumerate(pauli):
        if p == 'X':
            circuit << H(q[i])
        elif p == 'Y':
            circuit << RZ(q[i], -np.pi/2)
            circuit << H(q[i])

    if non_identity:
        target = non_identity[0]
        others = non_identity[1:]
        for j in others:
            circuit << CNOT(q[j], q[target])
        circuit << RZ(q[target], 2 * time)
        for j in reversed(others):
            circuit << CNOT(q[j], q[target])

    for i, p in enumerate(pauli):
        if p == 'X':
            circuit << H(q[i])
        elif p == 'Y':
            circuit << H(q[i])
            circuit << RZ(q[i], np.pi/2)

    return circuit

if __name__ == "__main__":
    machine.finalize()
