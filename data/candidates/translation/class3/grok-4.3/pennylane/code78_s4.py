# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    with qml.tape.QuantumTape() as tape:
        for j in reversed(range(num_qubits)):
            qml.Hadamard(wires=j)
            for i in reversed(range(j)):
                angle = -2 * np.pi / (2 ** (j - i))
                qml.ControlledPhaseShift(angle, wires=[j, i])
    return tape
