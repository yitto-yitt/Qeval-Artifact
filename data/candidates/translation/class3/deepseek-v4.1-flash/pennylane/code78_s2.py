# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    with qml.tape.QuantumTape() as tape:
        for i in reversed(range(num_qubits)):
            if i < num_qubits - 1:
                for j in reversed(range(i + 1, num_qubits)):
                    qml.ControlledPhaseShift(-np.pi / 2 ** (j - i), wires=[j, i])
            qml.Hadamard(wires=i)
    return tape
