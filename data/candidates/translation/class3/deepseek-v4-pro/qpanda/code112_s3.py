# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, RZ, CNOT
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = [Qubit() for _ in range(n)]
    circuit = QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        step_angle = 2 * time / reps
        for _ in range(reps):
            # Basis rotation to Z basis
            for i, ch in enumerate(pauli_string):
                if ch == 'X':
                    circuit.insert(H(qubits[i]))
                elif ch == 'Y':
                    circuit.insert(RZ(qubits[i], -math.pi / 2))
                    circuit.insert(H(qubits[i]))

            active = [i for i, ch in enumerate(pauli_string) if ch != 'I']

            # CNOT cascade to reduce multi-qubit Z to single qubit
            for idx in range(len(active) - 1):
                circuit.insert(CNOT(qubits[active[idx]], qubits[active[idx + 1]]))

            if active:
                circuit.insert(RZ(qubits[active[-1]], step_angle))

            # Uncompute CNOT cascade
            for idx in reversed(range(len(active) - 1)):
                circuit.insert(CNOT(qubits[active[idx]], qubits[active[idx + 1]]))

            # Undo basis rotation
            for i, ch in enumerate(pauli_string):
                if ch == 'X':
                    circuit.insert(H(qubits[i]))
                elif ch == 'Y':
                    circuit.insert(H(qubits[i]))
                    circuit.insert(RZ(qubits[i], math.pi / 2))

    return circuit
