# EVAL_META: task_id=12, framework=cirq, class=3
import cirq
import numpy as np


def get_unitary():
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    
    # Simulate the circuit to get the unitary matrix
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit, qubit_order=qubits)
    
    # Get the unitary by simulating the circuit directly
    unitary = circuit.unitary(qubit_order=qubits)
    return unitary
