# EVAL_META: task_id=78, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def qft_no_swaps(num_qubits):
    ops = []
    wires = list(range(num_qubits))

    with qml.QueuingManager.stop_recording():
        for target in range(num_qubits):
            for control in reversed(range(target)):
                angle = -np.pi / (2 ** (target - control))
                ops.append(qml.ControlledPhaseShift(angle, wires=[wires[control], wires[target]]))
            ops.append(qml.Hadamard(wires=wires[target]))

    return qml.tape.QuantumScript(ops)
