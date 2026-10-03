# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(20)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    circuit = QCircuit()
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            theta = time / reps
            qubit_indices = [i for i, p in enumerate(pauli_string) if p != 'I']
            if not qubit_indices:
                continue
            for i in qubit_indices:
                if pauli_string[i] == 'X':
                    circuit << H(qubits[i])
                elif pauli_string[i] == 'Y':
                    circuit << Sdag(qubits[i])
                    circuit << H(qubits[i])
            for i in range(len(qubit_indices) - 1):
                circuit << CNOT(qubits[qubit_indices[i]], qubits[qubit_indices[i+1]])
            last_qubit = qubit_indices[-1]
            circuit << RZ(qubits[last_qubit], 2 * theta)
            for i in reversed(range(len(qubit_indices) - 1)):
                circuit << CNOT(qubits[qubit_indices[i]], qubits[qubit_indices[i+1]])
            for i in reversed(qubit_indices):
                if pauli_string[i] == 'X':
                    circuit << H(qubits[i])
                elif pauli_string[i] == 'Y':
                    circuit << H(qubits[i])
                    circuit << S(qubits[i])
    return circuit

qvm.finalize()
