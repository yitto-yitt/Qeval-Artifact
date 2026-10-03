# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    qubits = cirq.LineQubit.range(2)
    ops = cirq.two_qubit_matrix_to_operations(qubits[0], qubits[1], unitary)
    new_ops = []
    for op in ops:
        if isinstance(op.gate, cirq.CZPowGate) and op.gate.exponent == 1:
            q0, q1 = op.qubits
            new_ops.extend([cirq.H(q1), cirq.CX(q0, q1), cirq.H(q1)])
        else:
            new_ops.append(op)
    return cirq.Circuit(new_ops)
