# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np

def create_operator():
    unitary = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.MatrixGate(np.array(unitary)).on(*qubits))
    decomposed = cirq.Circuit(cirq.decompose(circuit))
    return decomposed
