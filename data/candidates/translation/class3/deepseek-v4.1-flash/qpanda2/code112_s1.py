# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import math

qvm = CPUQVM()
qvm.init_qvm()

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qubits = qvm.qAlloc_many(n_qubits)
    circ = QCircuit()
    
    for pauli_str, time in zip(pauli_strings, times):
        theta = time / reps if reps > 0 else time
        for _ in range(reps):
            # Basis changes before Z-ladder
            for i, p in enumerate(pauli_str):
                if p == 'X':
                    circ << H(qubits[i])
                elif p == 'Y':
                    circ << RZ(qubits[i], -math.pi / 2) << H(qubits[i])
            # Z-ladder
            active = [i for i, p in enumerate(pauli_str) if p != 'I']
            if active:
                target = active[-1]
                for q in active[:-1]:
                    circ << CNOT(qubits[q], qubits[target])
                circ << RZ(qubits[target], 2 * theta)
                for q in reversed(active[:-1]):
                    circ << CNOT(qubits[q], qubits[target])
            # Basis changes after Z-ladder
            for i, p in enumerate(pauli_str):
                if p == 'X':
                    circ << H(qubits[i])
                elif p == 'Y':
                    circ << H(qubits[i]) << RZ(qubits[i], math.pi / 2)
    
    return circ

qvm.finalize()
