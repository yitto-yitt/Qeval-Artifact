# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def qft_no_swaps(num_qubits):
    with qml.queuing.QueuingManager.stop_recording():
        forward = []
        for j in reversed(range(num_qubits)):
            forward.append(qml.Hadamard(wires=j))
            for k in reversed(range(j)):
                lam = np.pi * (2.0 ** (k - j))
                forward.append(qml.ControlledPhaseShift(lam, wires=[j, k]))
        ops = [qml.adjoint(op) for op in reversed(forward)]
    return ops
