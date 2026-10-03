# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np


def create_operator():
    q0, q1 = cirq.LineQubit.range(2)
    unitary = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [0, 1, 0, 0],
         [1, 0, 0, 0]],
        dtype=complex,
    )
    circuit = cirq.Circuit(cirq.MatrixGate(unitary).on(q0, q1))
    optimized = cirq.optimize_for_target_gateset(
        circuit,
        gateset=cirq.CZTargetGateset(),
    )
    return optimized
