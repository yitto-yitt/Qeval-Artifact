# EVAL_META: task_id=112, framework=qpanda2, class=3
from math import pi
from pyqpanda import *

_machine = CPUQVM()
_machine.init_qvm()
_allocated_qubits = []


def _append_pauli_term(circ, q, pauli_string, time):
    active = [i for i, pauli in enumerate(pauli_string) if pauli != 'I']
    if not active:
        return

    # Basis change: map X and Y to Z
    for i in active:
        if pauli_string[i] == 'X':
            circ.insert(H(q[i]))
        elif pauli_string[i] == 'Y':
            circ.insert(RX(q[i], -pi / 2))

    # CNOT staircase
    for a, b in zip(active[:-1], active[1:]):
        circ.insert(CNOT(q[a], q[b]))

    circ.insert(RZ(q[active[-1]], 2 * time))

    # Inverse CNOT staircase
    for a, b in reversed(list(zip(active[:-1], active[1:]))):
        circ.insert(CNOT(q[a], q[b]))

    # Inverse basis change
    for i in reversed(active):
        if pauli_string[i] == 'X':
            circ.insert(H(q[i]))
        elif pauli_string[i] == 'Y':
            circ.insert(RX(q[i], pi / 2))


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    q = _machine.qAlloc_many(n)
    _allocated_qubits.append(q)

    circ = QCircuit()
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            _append_pauli_term(circ, q, pauli_string, time / reps)

    return circ


if __name__ == "__main__":
    _machine.finalize()
