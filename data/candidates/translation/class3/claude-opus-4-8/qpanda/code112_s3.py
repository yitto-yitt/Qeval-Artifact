# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, RX, RY, RZ, CNOT, H, S, X, Y, Z, RZZ

def create_product_formula_circuit(pauli_strings, times, order, reps):
    import math

    def append_pauli_evolution(circ, pauli_string, angle_total, reps):
        # pauli_string is given MSB-first (qubit n-1 ... 0), like Qiskit Pauli label.
        n = len(pauli_string)
        # Map label index i -> qubit index. Qiskit label leftmost char = highest qubit.
        # pauli_string[k] corresponds to qubit (n-1-k)
        terms = []
        for k, p in enumerate(pauli_string):
            q = n - 1 - k
            if p != 'I':
                terms.append((q, p))
        if not terms:
            return
        angle = angle_total / reps
        for _ in range(reps):
            # basis change
            for q, p in terms:
                if p == 'X':
                    circ << H(q)
                elif p == 'Y':
                    circ << RX(q, math.pi / 2)
            # CNOT ladder onto last qubit
            qubits = [q for q, _ in terms]
            for i in range(len(qubits) - 1):
                circ << CNOT(qubits[i], qubits[i + 1])
            # RZ rotation. PauliEvolutionGate uses exp(-i * time * P), giving RZ(2*time).
            circ << RZ(qubits[-1], 2.0 * angle)
            # undo CNOT ladder
            for i in range(len(qubits) - 2, -1, -1):
                circ << CNOT(qubits[i], qubits[i + 1])
            # undo basis change
            for q, p in terms:
                if p == 'X':
                    circ << H(q)
                elif p == 'Y':
                    circ << RX(q, -math.pi / 2)

    num_qubits = len(pauli_strings[0])
    circ = QCircuit(num_qubits)
    for pauli_string, time in zip(pauli_strings, times):
        append_pauli_evolution(circ, pauli_string, time, reps)
    return circ
