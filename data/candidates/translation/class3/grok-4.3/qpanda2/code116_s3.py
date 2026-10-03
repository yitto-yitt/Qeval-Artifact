# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(10)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    q = qubits[:n]
    circuit = QCircuit()
    for i in range(n):
        p = pauli_string[n - 1 - i]
        if p == 'X':
            circuit << H(q[i])
        elif p == 'Y':
            circuit << RX(q[i], -np.pi / 2)
    active_qubits = [i for i in range(n) if pauli_string[n - 1 - i] != 'I']
    if active_qubits:
        target = active_qubits[-1]
        for i in active_qubits[:-1]:
            circuit << CNOT(q[i], q[target])
        circuit << RZ(q[target], 2 * time)
        for i in reversed(active_qubits[:-1]):
            circuit << CNOT(q[i], q[target])
    for i in range(n - 1, -1, -1):
        p = pauli_string[n - 1 - i]
        if p == 'X':
            circuit << H(q[i])
        elif p == 'Y':
            circuit << RX(q[i], np.pi / 2)
    return circuit

machine.finalize()
