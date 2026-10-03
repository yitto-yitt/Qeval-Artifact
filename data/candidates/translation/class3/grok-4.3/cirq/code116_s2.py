# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np
from scipy.linalg import expm

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    qubits = cirq.LineQubit.range(n_qubits)
    pauli_ops = {'I': cirq.I, 'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}
    pauli_map = {}
    for i, p in enumerate(reversed(pauli_string)):
        if p != 'I':
            pauli_map[qubits[i]] = pauli_ops[p]
    ps = cirq.PauliString(pauli_map)
    pauli_matrix = ps.matrix(qubit_order=qubits)
    unitary = expm(-1j * time * pauli_matrix)
    gate = cirq.MatrixGate(unitary)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
