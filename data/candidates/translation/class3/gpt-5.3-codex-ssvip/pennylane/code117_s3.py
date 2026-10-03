# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def decompose_unitary(unitary):
    U = np.array(unitary, dtype=complex)
    if U.shape != (4, 4):
        raise ValueError("Input unitary must be a 4x4 matrix.")
    ops = qml.ops.two_qubit_decomposition(U, wires=[0, 1])
    return qml.tape.QuantumScript(ops=ops, measurements=[])
