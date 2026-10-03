# EVAL_META: task_id=112, framework=qpanda, class=3
import math
from pyqpanda3.core import QProg, H, RX, RZ, CNOT


def _apply_basis_change(prog, label, qubit, inverse):
    # Rotate the single-qubit Pauli into the Z (diagonal) basis.
    if label == 'X':
        prog << H(qubit)
    elif label == 'Y':
        prog << RX(qubit, -math.pi / 2.0 if inverse else math.pi / 2.0)


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    steps = int(reps) if reps else 1
    if steps < 1:
        steps = 1

    prog = QProg()

    for pauli_string, t in zip(pauli_strings, times):
        labels = [c.upper() for c in str(pauli_string) if not c.isspace()]
        active = [i for i, c in enumerate(labels) if c != 'I']
        if len(active) == 0:
            # exp(-i t I) is a pure global phase; nothing to append.
            continue

        dt = float(t) / float(steps)
        angle = 2.0 * dt

        for _ in range(steps):
            # Basis change: X -> H, Y -> RX(pi/2)
            for i in active:
                _apply_basis_change(prog, labels[i], i, False)

            # CNOT ladder: compute the parity onto the last active qubit.
            for a, b in zip(active[:-1], active[1:]):
                prog << CNOT(a, b)

            # exp(-i dt Z) on the parity qubit.
            prog << RZ(active[-1], angle)

            # Uncompute the CNOT ladder.
            rev = active[::-1]
            for a, b in zip(rev[:-1], rev[1:]):
                prog << CNOT(a, b)

            # Undo the basis change.
            for i in reversed(active):
                _apply_basis_change(prog, labels[i], i, True)

    return prog
