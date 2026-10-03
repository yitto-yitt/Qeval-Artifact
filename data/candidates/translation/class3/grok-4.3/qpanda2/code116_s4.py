# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qs = qubits[:n]
    circuit = QCircuit()
    active_indices = [i for i in range(n) if pauli_string[i] != 'I']
    active_qs = [qs[i] for i in active_indices]
    active_paulis = [pauli_string[i] for i in active_indices]
    m = len(active_qs)
    if m == 0:
        return circuit
    for idx, p in enumerate(active_paulis):
        if p == 'X':
            circuit << H(active_qs[idx])
        elif p == 'Y':
            circuit << RX(active_qs[idx], -np.pi/2)
    if m > 1:
        for i in range(m-1):
            circuit << CNOT(active_qs[i], active_qs[m-1])
        circuit << RZ(active_qs[m-1], 2 * time)
        for i in range(m-2, -1, -1):
            circuit << CNOT(active_qs[i], active_qs[m-1])
    else:
        circuit << RZ(active_qs[0], 2 * time)
    for idx in range(m-1, -1, -1):
        p = active_paulis[idx]
        if p == 'X':
            circuit << H(active_qs[idx])
        elif p == 'Y':
            circuit << RX(active_qs[idx], np.pi/2)
    return circuit

machine.finalize()
