# EVAL_META: task_id=117, framework=pennylane, class=3
import numpy as np
import pennylane as qml

try:
    from pennylane.ops import two_qubit_decomposition
except ImportError:
    from pennylane.ops.op_math.decompositions import two_qubit_decomposition


def decompose_unitary(unitary):
    U = np.asarray(unitary, dtype=complex)
    ops = two_qubit_decomposition(U, wires=[0, 1])
    return qml.tape.QuantumScript(ops=ops, measurements=[])
