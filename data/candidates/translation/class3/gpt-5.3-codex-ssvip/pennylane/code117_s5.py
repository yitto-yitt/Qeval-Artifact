# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def decompose_unitary(unitary):
    U = np.array(unitary, dtype=complex)
    if U.shape != (4, 4):
        raise ValueError("Input unitary must be a 4x4 matrix.")
    if not np.allclose(U.conj().T @ U, np.eye(4), atol=1e-8):
        raise ValueError("Input matrix must be unitary.")

    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(U, wires=[0, 1])
        return qml.state()

    _ = circuit()
    tape = circuit._tape
    decomposed_ops = qml.transforms.decompose(tape, gate_set={qml.CNOT, qml.RX, qml.RY, qml.RZ, qml.PhaseShift}).operations

    return qml.tape.QuantumScript(ops=decomposed_ops, measurements=[qml.state()])
