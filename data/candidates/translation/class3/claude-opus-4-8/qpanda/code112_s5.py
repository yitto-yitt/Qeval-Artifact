# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, RX, RY, RZ, H, CNOT

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qc = QCircuit(num_qubits)

    for pauli_string, time in zip(pauli_strings, times):
        # Qiskit Pauli string is little-endian: rightmost char is qubit 0
        chars = pauli_string[::-1]
        active = [i for i, c in enumerate(chars) if c != 'I']

        if not active:
            continue

        dt = time / reps
        for _ in range(reps):
            sub = QCircuit(num_qubits)
            # basis change to Z basis
            for i in active:
                c = chars[i]
                if c == 'X':
                    sub << H(i)
                elif c == 'Y':
                    sub << RX(i, 3.141592653589793 / 2)
            # CNOT ladder
            for k in range(len(active) - 1):
                sub << CNOT(active[k], active[k + 1])
            # rotation on last active qubit
            sub << RZ(active[-1], 2.0 * dt)
            # undo CNOT ladder
            for k in range(len(active) - 2, -1, -1):
                sub << CNOT(active[k], active[k + 1])
            # undo basis change
            for i in active:
                c = chars[i]
                if c == 'X':
                    sub << H(i)
                elif c == 'Y':
                    sub << RX(i, -3.141592653589793 / 2)
            qc << sub

    return qc
