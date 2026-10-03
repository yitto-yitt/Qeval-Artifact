# EVAL_META: task_id=116, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, I, H, RX, RZ, U3, CNOT


def synthesize_evolution_gate(pauli_string, time):
    if not pauli_string or any(p not in "IXYZ" for p in pauli_string):
        raise ValueError("pauli_string must be a nonempty string of I, X, Y, and Z.")

    circuit = QCircuit()
    paulis = list(reversed(pauli_string))
    active = [q for q, p in enumerate(paulis) if p != "I"]
    angle = 2.0 * float(time)

    for q in range(len(paulis)):
        circuit << I(q)

    if not active:
        circuit << RZ(0, angle)
        circuit << U3(0, 0.0, 0.0, -angle)
        return circuit

    for q in active:
        if paulis[q] == "X":
            circuit << H(q)
        elif paulis[q] == "Y":
            circuit << RX(q, pi / 2.0)

    target = active[-1]
    for q in active[:-1]:
        circuit << CNOT(q, target)

    circuit << RZ(target, angle)

    for q in reversed(active[:-1]):
        circuit << CNOT(q, target)

    for q in reversed(active):
        if paulis[q] == "X":
            circuit << H(q)
        elif paulis[q] == "Y":
            circuit << RX(q, -pi / 2.0)

    return circuit
