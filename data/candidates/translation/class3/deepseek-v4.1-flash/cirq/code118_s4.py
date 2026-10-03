# EVAL_META: task_id=118, framework=cirq, class=3
import cirq
import numpy as np

def create_c3sx_circuit():
    qubits = [cirq.LineQubit(i) for i in range(4)]
    sx_matrix = np.array([[0.5+0.5j, 0.5-0.5j],
                          [0.5-0.5j, 0.5+0.5j]], dtype=complex)
    sx_gate = cirq.MatrixGate(sx_matrix)
    c3sx_gate = cirq.ControlledGate(sx_gate, num_controls=3)
    circuit = cirq.Circuit(c3sx_gate(*qubits))
    return circuit
