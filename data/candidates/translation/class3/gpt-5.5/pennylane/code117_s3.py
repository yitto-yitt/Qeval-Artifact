# EVAL_META: task_id=117, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def decompose_unitary(unitary):
    U = np.asarray(getattr(unitary, "data", unitary), dtype=complex)
    wires = [0, 1]

    try:
        return qml.ops.two_qubit_decomposition(U, wires=wires)
    except AttributeError:
        pass

    try:
        from pennylane.ops.qubit.decompositions import two_qubit_decomposition
        return two_qubit_decomposition(U, wires=wires)
    except Exception:
        return qml.QubitUnitary.compute_decomposition(U, wires=wires)
