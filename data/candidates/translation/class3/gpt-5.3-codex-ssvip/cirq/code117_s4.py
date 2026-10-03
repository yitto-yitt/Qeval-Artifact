# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np


def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    matrix = np.asarray(unitary, dtype=complex)
    op = cirq.MatrixGate(matrix).on(q0, q1)
    circuit = cirq.Circuit(cirq.decompose(op, keep=lambda o: isinstance(o.gate, (cirq.CNotPowGate, cirq.XPowGate, cirq.YPowGate, cirq.ZPowGate, cirq.PhasedXPowGate))))
    return circuit
