# EVAL_META: task_id=12, framework=cirq, class=3
import cirq
import numpy as np


def get_unitary():
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    
    # Get the unitary matrix by simulating the circuit
    unitary = cirq.unitary(circuit)
    return unitary
