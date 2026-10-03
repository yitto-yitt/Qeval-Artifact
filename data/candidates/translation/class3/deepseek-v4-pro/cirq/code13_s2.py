# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    q = cirq.LineQubit(0)
    unitary = np.array([[1, -1j], [1j, -1]]) / np.sqrt(2)
    circuit = cirq.Circuit(cirq.MatrixGate(unitary).on(q))
    return circuit
