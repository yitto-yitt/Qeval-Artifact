# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

qvm = CPUQVM()
qvm.init_qvm()

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = qvm.qAlloc_many(n)
    circuit = QCircuit()
    S = [i for i, p in enumerate(pauli_string) if p != 'I']
    if not S:
        return circuit
    target = S[0]
    for i, p in enumerate(pauli_string):
        if p == 'X':
            circuit << H(qubits[i])
        elif p == 'Y':
            circuit << RZ(qubits[i], -np.pi/2)
            circuit << H(qubits[i])
    for i in S:
        if i != target:
            circuit << CNOT(qubits[i], qubits[target])
    circuit << RZ(qubits[target], 2 * time)
    for i in reversed(S):
        if i != target:
            circuit << CNOT(qubits[i], qubits[target])
    for i, p in enumerate(pauli_string):
        if p == 'X':
            circuit << H(qubits[i])
        elif p == 'Y':
            circuit << H(qubits[i])
            circuit << RZ(qubits[i], np.pi/2)
    return circuit

if __name__ == "__main__":
    qvm.finalize()
