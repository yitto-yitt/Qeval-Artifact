# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    wires = list(range(num_qubits))
    with qml.tape.QuantumTape() as tape:
        for i in range(num_qubits):
            qml.Hadamard(wires=wires[i])
            for j in range(i + 1, num_qubits):
                qml.ControlledPhaseShift(
                    -np.pi / (2 ** (j - i)),
                    wires=[wires[j], wires[i]]
                )
    return tape
