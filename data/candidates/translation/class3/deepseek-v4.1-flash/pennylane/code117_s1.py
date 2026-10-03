# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def decompose_unitary(unitary):
    ops, phase = qml.transforms.two_qubit_decomposition(
        unitary, wires=[0, 1], return_global_phase=True
    )
    ops.append(qml.GlobalPhase(phase, wires=[0, 1]))
    return QuantumScript(ops, [])
