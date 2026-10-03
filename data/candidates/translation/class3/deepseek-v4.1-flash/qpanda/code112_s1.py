# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, RX, RZ, CNOT
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qc = QCircuit()
    qubits = [Qubit(i) for i in range(n)]
    for pauli_str, time in zip(pauli_strings, times):
        for _ in range(reps):
            t = time / reps
            active = []
            for i, ch in enumerate(pauli_str):
                if ch != 'I':
                    active.append(i)
            if not active:
                continue
            for i in active:
                ch = pauli_str[i]
                if ch == 'X':
                    qc << H(qubits[i])
                elif ch == 'Y':
                    qc << RX(qubits[i], math.pi / 2)
            for i in range(len(active) - 1):
                qc << CNOT(qubits[active[i]], qubits[active[i+1]])
            qc << RZ(qubits[active[-1]], 2 * t)
            for i in range(len(active) - 2, -1, -1):
                qc << CNOT(qubits[active[i]], qubits[active[i+1]])
            for i in active:
                ch = pauli_str[i]
                if ch == 'X':
                    qc << H(qubits[i])
                elif ch == 'Y':
                    qc << RX(qubits[i], -math.pi / 2)
    return qc
