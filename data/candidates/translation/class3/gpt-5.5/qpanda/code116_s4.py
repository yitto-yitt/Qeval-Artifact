# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def synthesize_evolution_gate(pauli_string, time):
    circuit = QCircuit()
    n = len(pauli_string)

    for q in range(n):
        circuit << I(q)

    active_qubits = []

    for q, p in enumerate(reversed(pauli_string)):
        if p == "X":
            circuit << H(q)
            active_qubits.append(q)
        elif p == "Y":
            circuit << RX(q, math.pi / 2)
            active_qubits.append(q)
        elif p == "Z":
            active_qubits.append(q)
        elif p == "I":
            continue
        else:
            raise ValueError("Pauli string can only contain 'I', 'X', 'Y', and 'Z'.")

    if active_qubits:
        target = active_qubits[-1]

        for q in active_qubits[:-1]:
            circuit << CNOT(q, target)

        circuit << RZ(target, 2 * time)

        for q in reversed(active_qubits[:-1]):
            circuit << CNOT(q, target)

    for q, p in reversed(list(enumerate(reversed(pauli_string)))):
        if p == "X":
            circuit << H(q)
        elif p == "Y":
            circuit << RX(q, -math.pi / 2)

    return circuit
