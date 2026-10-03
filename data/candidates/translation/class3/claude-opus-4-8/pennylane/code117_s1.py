# EVAL_META: task_id=117, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def decompose_unitary(unitary):
    if hasattr(unitary, "data"):
        U = np.asarray(unitary.data)
    elif hasattr(unitary, "to_matrix"):
        U = np.asarray(unitary.to_matrix())
    else:
        U = np.asarray(unitary)

    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(U, wires=[0, 1])
        return qml.state()

    tape = qml.workflow.construct_tape(circuit)()
    decomposed = qml.transforms.decompose(
        tape, gate_set={"CNOT", "RX", "RY", "RZ", "Rot", "GlobalPhase"}
    )
    ops = decomposed[0][0].operations
    return ops
