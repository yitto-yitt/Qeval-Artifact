# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    operations = cirq.two_qubit_matrix_to_operations(q0, q1, unitary, allow_partial_czs=False)
    return cirq.Circuit(operations)
