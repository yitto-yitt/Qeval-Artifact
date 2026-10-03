# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    theta = 0.3
    phi = 0.2
    lam = 0.1
    
    cos_val = np.cos(theta / 2)
    sin_val = np.sin(theta / 2)
    
    matrix = np.array([
        [cos_val, -np.exp(1j * lam) * sin_val],
        [np.exp(1j * phi) * sin_val, np.exp(1j * (phi + lam)) * cos_val]
    ], dtype=np.complex128)
    
    custom_gate = cirq.MatrixGate(matrix)
    controlled_gate = custom_gate.controlled(num_controls=1)
    
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(controlled_gate(qubits[0], qubits[1]))
    
    return circuit
