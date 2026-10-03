# EVAL_META: task_id=116, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, H, RZ, CNOT

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qc = QCircuit()

    active = [i for i, p in enumerate(pauli_string) if p.upper() != 'I']
    active_set = set(active)

    # Ensure the circuit has all required qubits, including identity-only wires.
    for i in range(n):
        if i not in active_set:
            qc << RZ(i, 0.0)

    if not active:
        return qc

    # Change to Z basis: X -> H, Y -> Sdg then H (here Sdg is RZ(-pi/2)).
    for idx in active:
        p = pauli_string[idx].upper()
        if p == 'X':
            qc << H(idx)
        elif p == 'Y':
            qc << RZ(idx, -math.pi / 2)
            qc << H(idx)

    # Parity CNOT ladder.
    for j in range(len(active) - 1):
        qc << CNOT(active[j], active[j + 1])

    qc << RZ(active[-1], 2.0 * time)

    for j in range(len(active) - 2, -1, -1):
        qc << CNOT(active[j], active[j + 1])

    # Undo basis change.
    for idx in reversed(active):
        p = pauli_string[idx].upper()
        if p == 'X':
            qc << H(idx)
        elif p == 'Y':
            qc << H(idx)
            qc << RZ(idx, math.pi / 2)

    return qc
