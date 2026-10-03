# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np

def create_operator():
    XX = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    circ = cirq.Circuit()
    q0, q1 = cirq.LineQubit.range(2)
    circ.append(cirq.MatrixGate(XX).on(q0, q1))
    decomposed_circ = cirq.Circuit(cirq.decompose(circ))
    return decomposed_circ
