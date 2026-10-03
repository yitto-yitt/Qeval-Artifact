# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *

def synthesize_evolution_gate(pauli_string, time):
    pauli_string = pauli_string.upper()
    n = len(pauli_string)
    if n == 0:
        return QCircuit()

    try:
        init()
    except NameError:
        init_qvm()

    try:
        qubits = qAlloc_many(n)
    except NameError:
        qubits = qalloc(n)

    qc = QCircuit()

    non_identity = [i for i, p in enumerate(pauli_string) if p != 'I']

    # Change Pauli X/Y to Z basis.
    for i, p in enumerate(pauli_string):
        if p == 'X':
            qc << H(qubits[i])
        elif p == 'Y':
            qc << RZ(qubits[i], -np.pi / 2)
            qc << H(qubits[i])

    # Compute parity of the non-identity qubits into the last one.
    for idx in range(len(non_identity) - 1):
        qc << CNOT(qubits[non_identity[idx]], qubits[non_identity[idx + 1]])

    if non_identity:
        qc << RZ(qubits[non_identity[-1]], 2.0 * time)

    # Uncompute the parity chain.
    for idx in range(len(non_identity) - 2, -1, -1):
        qc << CNOT(qubits[non_identity[idx]], qubits[non_identity[idx + 1]])

    # Restore original basis.
    for i in range(n - 1, -1, -1):
        p = pauli_string[i]
        if p == 'X':
            qc << H(qubits[i])
        elif p == 'Y':
            qc << H(qubits[i])
            qc << RZ(qubits[i], np.pi / 2)

    return qc
