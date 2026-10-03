# EVAL_META: task_id=78, framework=pennylane, class=3
import math
import pennylane as qml


def qft_no_swaps(num_qubits):
    operations = []
    for target in range(num_qubits):
        for control in range(target):
            angle = -math.pi / (2 ** (target - control))
            operations.append(
                qml.ControlledPhaseShift(angle, wires=[target, control])
            )
        operations.append(qml.Hadamard(wires=target))
    return qml.tape.QuantumScript(operations)
