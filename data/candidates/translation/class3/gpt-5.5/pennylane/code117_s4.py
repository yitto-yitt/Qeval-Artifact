# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def decompose_unitary(unitary):
    U = np.asarray(getattr(unitary, "data", unitary), dtype=complex)
    ops = qml.QubitUnitary.compute_decomposition(U, wires=[0, 1])
    return qml.tape.QuantumScript(ops, [])
