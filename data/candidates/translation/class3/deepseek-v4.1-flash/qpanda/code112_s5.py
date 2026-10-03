# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, RZ
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    circuit = QCircuit()
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            non_id_qubits = [i for i, p in enumerate(pauli_string) if p != 'I']
            if not non_id_qubits:
                continue
            for i in non_id_qubits:
                p = pauli_string[i]
                if p == 'X':
                    circuit << H(i)
                elif p == 'Y':
                    circuit << RZ(i, -math.pi / 2)
                    circuit << H(i)
            for i in range(len(non_id_qubits) - 1):
                circuit << CNOT(non_id_qubits[i], non_id_qubits[i + 1])
            last = non_id_qubits[-1]
            circuit << RZ(last, 2 * time)
            for i in range(len(non_id_qubits) - 2, -1, -1):
                circuit << CNOT(non_id_qubits[i], non_id_qubits[i + 1])
            for i in reversed(non_id_qubits):
                p = pauli_string[i]
                if p == 'X':
                    circuit << H(i)
                elif p == 'Y':
                    circuit << H(i)
                    circuit << RZ(i, math.pi / 2)
    return circuit
