# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np

def create_operator():
    unitary = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    qubits = cirq.LineQubit.range(2)
    circ = cirq.Circuit(cirq.MatrixGate(unitary).on(*qubits))
    decomposed = cirq.decompose(circ)
    optimized = cirq.optimize_for_target_gateset(decomposed, gateset=cirq.CNOTTargetGateset())
    return optimized
