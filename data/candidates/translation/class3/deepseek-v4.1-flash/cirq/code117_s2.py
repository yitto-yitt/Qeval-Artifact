# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    unitary = np.asarray(unitary)
    ops = cirq.two_qubit_matrix_to_operations(q0, q1, unitary, allow_partial_czs=False)
    converted_ops = []
    for op in ops:
        if isinstance(op.gate, cirq.CZPowGate):
            qa, qb = op.qubits
            converted_ops.append(cirq.H(qb))
            converted_ops.append(cirq.CNOT(qa, qb))
            converted_ops.append(cirq.H(qb))
        else:
            converted_ops.append(op)
    return cirq.Circuit(converted_ops)
