# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, RX, RZ, CNOT

def create_product_formula_circuit(pauli_strings, times, order, reps):
    nq = len(pauli_strings[0])
    qc = QCircuit(nq)

    def append_pauli_evolution(circ, pauli_string, angle):
        n = len(pauli_string)
        # Qiskit Pauli string is little-endian: rightmost char -> qubit 0
        terms = []
        for i, p in enumerate(pauli_string):
            qubit = n - 1 - i
            if p != 'I':
                terms.append((qubit, p))
        if not terms:
            return
        # basis change to Z
        for qubit, p in terms:
            if p == 'X':
                circ << H(qubit)
            elif p == 'Y':
                circ << RX(qubit, 1.5707963267948966)
        # CNOT ladder
        qubits = [q for q, _ in terms]
        for i in range(len(qubits) - 1):
            circ << CNOT(qubits[i], qubits[i + 1])
        # RZ on last qubit; PauliEvolutionGate uses 2*time as RZ angle
        circ << RZ(qubits[-1], 2.0 * angle)
        # undo CNOT ladder
        for i in reversed(range(len(qubits) - 1)):
            circ << CNOT(qubits[i], qubits[i + 1])
        # undo basis change
        for qubit, p in terms:
            if p == 'X':
                circ << H(qubit)
            elif p == 'Y':
                circ << RX(qubit, -1.5707963267948966)

    for pauli_string, time in zip(pauli_strings, times):
        per_rep = time / reps
        for _ in range(reps):
            append_pauli_evolution(qc, pauli_string, per_rep)

    return qc
