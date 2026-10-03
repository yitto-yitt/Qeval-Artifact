# EVAL_META: task_id=112, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, Qubit, H, RX, RZ, CNOT

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(n)]
    
    for pauli_str, time in zip(pauli_strings, times):
        for _ in range(reps):
            t_rep = time / reps
            non_id = [i for i, c in enumerate(pauli_str) if c != 'I']
            if not non_id:
                continue
            for i in non_id:
                c = pauli_str[i]
                if c == 'X':
                    circuit << H(qubits[i])
                elif c == 'Y':
                    circuit << RX(qubits[i], math.pi / 2)
            for i in range(len(non_id) - 1):
                circuit << CNOT(qubits[non_id[i]], qubits[non_id[i+1]])
            last = non_id[-1]
            circuit << RZ(qubits[last], 2 * t_rep)
            for i in range(len(non_id) - 2, -1, -1):
                circuit << CNOT(qubits[non_id[i]], qubits[non_id[i+1]])
            for i in non_id:
                c = pauli_str[i]
                if c == 'X':
                    circuit << H(qubits[i])
                elif c == 'Y':
                    circuit << RX(qubits[i], -math.pi / 2)
    return circuit
