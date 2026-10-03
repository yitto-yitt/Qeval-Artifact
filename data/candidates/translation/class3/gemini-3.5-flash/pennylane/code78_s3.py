# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    def qft_forward_no_swaps(n):
        for i in range(n):
            qml.Hadamard(wires=i)
            for j in range(i + 1, n):
                angle = np.pi / (2 ** (j - i))
                qml.ControlledPhaseShift(angle, wires=[j, i])
    
    qml.adjoint(qft_forward_no_swaps)(num_qubits)
