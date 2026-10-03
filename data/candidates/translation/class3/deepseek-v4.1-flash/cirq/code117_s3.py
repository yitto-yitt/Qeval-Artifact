# EVAL_META: task_id=117, framework=cirq, class=3
import cirq

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    ops = cirq.two_qubit_matrix_to_cz_operations(q0, q1, unitary, allow_partial_czs=False)
    converted_ops = []
    for op in ops:
        if isinstance(op.gate, cirq.CZPowGate) and op.gate.exponent == 1:
            converted_ops.append(cirq.H(q1))
            converted_ops.append(cirq.CNOT(q0, q1))
            converted_ops.append(cirq.H(q1))
        else:
            converted_ops.append(op)
    return cirq.Circuit(converted_ops)
