# EVAL_META: task_id=117, framework=cirq, class=3
import cirq

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    ops = cirq.two_qubit_matrix_to_operations(q0, q1, unitary, allow_partial_cz=False)
    return cirq.Circuit(ops)
