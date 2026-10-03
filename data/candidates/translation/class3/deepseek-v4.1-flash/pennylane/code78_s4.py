# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def qft_no_swaps(num_qubits):
    ops = []
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            angle = -3.141592653589793 / (2 ** (j - i))
            ops.append(qml.ControlledPhaseShift(phi=angle, wires=[j, i]))
        ops.append(qml.Hadamard(wires=i))
    return QuantumScript(ops)
