# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    # Convert the 4x4 unitary matrix to a Cirq circuit
    # Using KAK decomposition which is equivalent to what Qiskit's TwoQubitBasisDecomposer does with CX gates
    kak_decomposition = cirq.kak_decomposition(unitary)
    
    # Create a circuit with 2 qubits
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    
    # Add the decomposition components
    # Pre-rotation
    circuit.append([cirq.MatrixGate(kak_decomposition.single_qubit_operations_before[0]).on(qubits[0]),
                    cirq.MatrixGate(kak_decomposition.single_qubit_operations_before[1]).on(qubits[1])])
    
    # Entangling operations
    circuit.append(cirq.Circuit([
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.ZPowGate(exponent=kak_decomposition.interaction_coefficients[0]/np.pi).on(qubits[1]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.YPowGate(exponent=kak_decomposition.interaction_coefficients[1]/np.pi).on(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.XPowGate(exponent=kak_decomposition.interaction_coefficients[2]/np.pi).on(qubits[1]),
        cirq.CNOT(qubits[0], qubits[1])
    ]))
    
    # Post-rotation
    circuit.append([cirq.MatrixGate(kak_decomposition.single_qubit_operations_after[0]).on(qubits[0]),
                    cirq.MatrixGate(kak_decomposition.single_qubit_operations_after[1]).on(qubits[1])])
    
    return circuit
