# EVAL_META: task_id=117, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def decompose_unitary(unitary):
    if hasattr(unitary, "to_matrix"):
        unitary = unitary.to_matrix()
    matrix = np.asarray(unitary, dtype=complex)

    with qml.QueuingManager.stop_recording():
        operations = list(qml.ops.two_qubit_decomposition(matrix, wires=[0, 1]))
        circuit = qml.tape.QuantumScript(operations)
        reconstructed = qml.matrix(circuit, wire_order=[0, 1])
        phase = np.angle(np.trace(reconstructed.conj().T @ matrix))
        operations.append(qml.GlobalPhase(-phase))
        return qml.tape.QuantumScript(operations)
