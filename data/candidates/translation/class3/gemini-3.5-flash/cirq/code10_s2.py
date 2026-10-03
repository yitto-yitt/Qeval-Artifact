# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np

def create_operator():
    q0, q1 = cirq.LineQubit.range(2)
    matrix = np.array([[0, 0, 0, 1], 
                       [0, 0, 1, 0], 
                       [0, 1, 0, 0], 
                       [1, 0, 0, 0]], dtype=np.complex128)
    ops = cirq.two_qubit_matrix_to_operations(q0, q1, matrix)
    return cirq.Circuit(ops)
