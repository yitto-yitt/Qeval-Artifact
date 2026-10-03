# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(cirq.MatrixGate(cirq.unitary(cirq.qis.QuantumFourierTransformGate(1)) @ np.array([[1, 0], [0, 1]], dtype=complex))(q))
    circuit = cirq.Circuit(cirq.MatrixGate(np.array([
        [np.cos(np.pi/4), -np.exp(1j*np.pi/2)*np.sin(np.pi/4)],
        [np.exp(1j*np.pi/2)*np.sin(np.pi/4), np.exp(1j*(np.pi/2+np.pi/2))*np.cos(np.pi/4)]
    ], dtype=complex))(q))
    return circuit
