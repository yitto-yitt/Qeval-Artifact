# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    def circuit():
        ops = []
        for j in range(num_qubits):
            ops.append(qml.Hadamard(wires=j))
            for k in range(j + 1, num_qubits):
                angle = np.pi / (2 ** (k - j))
                ops.append(qml.ControlledPhaseShift(angle, wires=[k, j]))
        adjoint_ops = [qml.adjoint(op) for op in reversed(ops)]
        return adjoint_ops
    return circuit
