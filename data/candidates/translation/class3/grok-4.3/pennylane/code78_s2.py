# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    wires = list(range(num_qubits))
    ops = []
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            phi = 2 * np.pi / 2 ** (j - i)
            ops.append(qml.ControlledPhaseShift(-phi, wires=[wires[j], wires[i]]))
        ops.append(qml.Hadamard(wires[i]))
    return qml.tape.QuantumScript(ops)
