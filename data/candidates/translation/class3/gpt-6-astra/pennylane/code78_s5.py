# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
from math import pi

def qft_no_swaps(num_qubits):
    operations = []
    with qml.QueuingManager.stop_recording():
        for j in range(num_qubits):
            for k in range(j):
                operations.append(
                    qml.ControlledPhaseShift(
                        -pi / (2 ** (j - k)), wires=[j, k]
                    )
                )
            operations.append(qml.Hadamard(wires=j))
    return qml.tape.QuantumScript(operations)
