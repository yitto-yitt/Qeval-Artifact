# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    qubits = cirq.LineQubit.range(2)
    theta, phi, lam = 0.3, 0.2, 0.1
    matrix = np.array([
        [np.cos(theta/2), -np.exp(1j*lam)*np.sin(theta/2)],
        [np.exp(1j*phi)*np.sin(theta/2), np.exp(1j*(phi+lam))*np.cos(theta/2)]
    ], dtype=np.complex128)
    
    u3_gate = cirq.MatrixGate(matrix)
    controlled_gate = u3_gate.controlled()
    
    circuit = cirq.Circuit(controlled_gate(qubits[0], qubits[1]))
    return circuit
