# EVAL_META: task_id=66, framework=cirq, class=2
import cirq
import numpy as np


def w_state():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    # Apply Ry gate with angle 2*arccos(1/sqrt(3)) to qubit 0
    angle = 2 * np.arccos(1 / np.sqrt(3))
    circuit.append(cirq.ry(angle).on(qubits[0]))
    
    # Apply controlled-Hadamard from qubit 0 to qubit 1
    circuit.append(cirq.ControlledGate(cirq.H).on(qubits[0], qubits[1]))
    
    # Apply CNOT from qubit 1 to qubit 2
    circuit.append(cirq.CNOT(qubits[1], qubits[2]))
    
    # Apply CNOT from qubit 0 to qubit 1
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    
    # Apply X gate to qubit 0
    circuit.append(cirq.X(qubits[0]))
    
    # Add measurements to all qubits
    circuit.append(cirq.measure(*qubits, key='result'))
    
    return circuit
