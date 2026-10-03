# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    wires = list(range(num_qubits))
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            angle = -2 * np.pi / (2 ** (j - i + 1))
            qml.ControlledPhaseShift(angle, wires=[wires[j], wires[i]])
        qml.Hadamard(wires=wires[i])
