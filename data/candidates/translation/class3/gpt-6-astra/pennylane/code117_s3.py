# EVAL_META: task_id=117, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=complex)
    operations = qml.ops.two_qubit_decomposition(matrix, wires=[0, 1])
    return qml.tape.QuantumScript(operations)
