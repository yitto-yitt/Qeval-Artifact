# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def qft_no_swaps(num_qubits):
    wires = list(range(num_qubits))

    forward = []
    for j in range(num_qubits):
        forward.append(("H", j))
        for k in range(j + 1, num_qubits):
            angle = np.pi / (2 ** (k - j))
            forward.append(("CP", angle, k, j))

    with qml.tape.QuantumTape() as tape:
        for op in reversed(forward):
            if op[0] == "H":
                qml.Hadamard(wires=op[1])
            else:
                _, angle, c, t = op
                qml.ControlledPhaseShift(-angle, wires=[c, t])

    return tape
