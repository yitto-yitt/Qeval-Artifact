# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    def forward_qft():
        for i in reversed(range(num_qubits)):
            qml.Hadamard(wires=i)
            for j in reversed(range(i)):
                angle = np.pi / (2 ** (i - j))
                qml.ControlledPhaseShift(angle, wires=[j, i])
    return qml.adjoint(forward_qft)
