# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np


def create_operator():
    q0, q1 = cirq.LineQubit.range(2)
    xx_matrix = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [0, 1, 0, 0],
         [1, 0, 0, 0]],
        dtype=np.complex128,
    )
    xx_gate = cirq.MatrixGate(xx_matrix)
    circuit = cirq.Circuit(xx_gate.on(q0, q1))
    optimized_circuit = cirq.optimize_for_target_gateset(
        circuit,
        gateset=cirq.CZTargetGateset(),
        ignore_failures=False,
    )
    return optimized_circuit
