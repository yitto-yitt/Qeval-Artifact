# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

def controlled_custom_unitary_circuit():
    # Define the custom unitary gate using the U3 parameters
    theta, phi, lam = 0.3, 0.2, 0.1
    custom_unitary = cirq.unitary(cirq.MatrixGate(np.array([
        [np.cos(theta/2), -np.exp(1j*lam)*np.sin(theta/2)],
        [np.exp(1j*phi)*np.sin(theta/2), np.exp(1j*(phi+lam))*np.cos(theta/2)]
    ])))
    
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Create the circuit with controlled custom unitary
    circuit = cirq.Circuit(
        cirq.ControlledGate(cirq.MatrixGate(custom_unitary)).on(q0, q1)
    )
    
    return circuit
