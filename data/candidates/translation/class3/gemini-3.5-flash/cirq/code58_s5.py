# EVAL_META: task_id=58, framework=cirq, class=3
import cirq
import numpy as np

def create_ch_gate():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.ry(np.pi/4)(qubits[1]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.ry(-np.pi/4)(qubits[1]))
    return circuit
