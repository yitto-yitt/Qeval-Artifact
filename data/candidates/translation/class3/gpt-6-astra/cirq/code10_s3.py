# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np

def create_operator():
    matrix = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [0, 1, 0, 0],
         [1, 0, 0, 0]],
        dtype=complex,
    )
    phase, first, second = cirq.kron_factor_4x4_to_2x2s(matrix)
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(
        cirq.MatrixGate(phase * first).on(q0),
        cirq.MatrixGate(second).on(q1),
    )
