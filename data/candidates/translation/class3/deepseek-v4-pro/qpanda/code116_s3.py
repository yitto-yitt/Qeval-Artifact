# EVAL_META: task_id=116, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QuantumCircuit


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qc = QuantumCircuit(n)

    active_qubits = [i for i, p in enumerate(pauli_string) if p.upper() != 'I']

    for qubit in active_qubits:
        p = pauli_string[qubit].upper()
        if p == 'X':
            qc.h(qubit)
        elif p == 'Y':
            qc.rx(qubit, pi / 2)

    for idx in range(len(active_qubits) - 1):
        qc.cnot(active_qubits[idx], active_qubits[idx + 1])

    if active_qubits:
        qc.rz(active_qubits[-1], 2 * time)

    for idx in range(len(active_qubits) - 2, -1, -1):
        qc.cnot(active_qubits[idx], active_qubits[idx + 1])

    for qubit in reversed(active_qubits):
        p = pauli_string[qubit].upper()
        if p == 'X':
            qc.h(qubit)
        elif p == 'Y':
            qc.rx(qubit, -pi / 2)

    return qc
