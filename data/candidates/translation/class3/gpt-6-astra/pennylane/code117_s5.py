# EVAL_META: task_id=117, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=complex)
    tape = qml.tape.QuantumScript(
        [qml.QubitUnitary(matrix, wires=[0, 1])]
    )
    decomposed_tapes, _ = qml.transforms.decompose(
        tape,
        gate_set={qml.CNOT, qml.RX, qml.RY, qml.RZ, qml.GlobalPhase},
    )
    return decomposed_tapes[0]
