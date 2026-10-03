# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    qubits = cirq.LineQubit.range(2)
    
    # Convert unitary to a cirq operation using MatrixGate
    unitary_op = cirq.MatrixGate(np.array(unitary), qid_shape=(2, 2))
    
    # Decompose the unitary into basic gates
    # cirq's two_qubit_matrix_to_cz_operations or manual decomposition
    # Using kak decomposition for two-qubit unitaries
    kak = cirq.kak_decomposition(unitary_op._unitary_)
    
    circuit = cirq.Circuit()
    # Apply single-qubit gates and CZ from KAK decomposition
    # KAK gives: single qubit gates around CZ interactions
    circuit.append(kak.single_qubit_operations_after[1].on(qubits[1]))
    circuit.append(kak.single_qubit_operations_after[0].on(qubits[0]))
    circuit.append(cirq.CZ(qubits[0], qubits[1]))
    circuit.append(kak.interaction_coefficients[0] * cirq.XX(qubits[0], qubits[1]))
    circuit.append(kak.interaction_coefficients[1] * cirq.YY(qubits[0], qubits[1]))
    circuit.append(kak.interaction_coefficients[2] * cirq.ZZ(qubits[0], qubits[1]))
    circuit.append(kak.single_qubit_operations_before[1].on(qubits[1]))
    circuit.append(kak.single_qubit_operations_before[0].on(qubits[0]))
    
    return circuit
