# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def decompose_unitary(unitary):
    with QuantumTape() as tape:
        qml.QubitUnitary(unitary, wires=[0, 1])
    res = qml.transforms.two_qubit_decomposition(tape)
    if isinstance(res, tuple):
        tapes = res[0]
    else:
        tapes = res
    if isinstance(tapes, list):
        return tapes[0] if len(tapes) == 1 else tapes
    return tapes
