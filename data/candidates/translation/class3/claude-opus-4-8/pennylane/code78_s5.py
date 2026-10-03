# EVAL_META: task_id=78, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def qft_no_swaps(num_qubits):
    ops = []
    for j in reversed(range(num_qubits)):
        ops.append(qml.Hadamard(wires=j))
        for k in reversed(range(j)):
            lam = np.pi * (2.0 ** (k - j))
            ops.append(qml.ControlledPhaseShift(lam, wires=[j, k]))
    inverse_ops = [qml.adjoint(op) for op in reversed(ops)]
    return inverse_ops
