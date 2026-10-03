# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, RZ, RX, RY, H, CNOT, S

def create_product_formula_circuit(pauli_strings, times, order, reps):
    def num_qubits(ps):
        return len(ps)

    n = num_qubits(pauli_strings[0])
    circ = QCircuit(n)

    for pauli_string, time in zip(pauli_strings, times):
        # Qiskit Pauli string is little-endian: rightmost char is qubit 0
        s = pauli_string[::-1]
        active = [(i, p) for i, p in enumerate(s) if p != 'I']

        dt = float(time) / reps

        for _ in range(reps):
            if not active:
                continue

            # Basis change to Z
            for i, p in active:
                if p == 'X':
                    circ << H(i)
                elif p == 'Y':
                    circ << RX(i, 1.5707963267948966)

            # CNOT ladder
            idxs = [i for i, _ in active]
            for k in range(len(idxs) - 1):
                circ << CNOT(idxs[k], idxs[k + 1])

            # RZ on last qubit: exp(-i * time * Z) -> RZ(2*time)
            circ << RZ(idxs[-1], 2.0 * dt)

            # Undo CNOT ladder
            for k in reversed(range(len(idxs) - 1)):
                circ << CNOT(idxs[k], idxs[k + 1])

            # Undo basis change
            for i, p in active:
                if p == 'X':
                    circ << H(i)
                elif p == 'Y':
                    circ << RX(i, -1.5707963267948966)

    return circ
