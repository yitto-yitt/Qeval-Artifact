# EVAL_META: task_id=78, framework=pennylane, class=3
import math
import pennylane as qml

def qft_no_swaps(num_qubits):
    for i in range(num_qubits):
        qml.Hadamard(wires=i)
        for j in range(i + 1, num_qubits):
            qml.ControlledPhaseShift(-math.pi / (2 ** (j - i)), wires=[i, j])
