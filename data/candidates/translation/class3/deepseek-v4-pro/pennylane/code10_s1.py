# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def create_operator():
    mat = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], dtype=complex)
    with qml.queuing.AnnotatedQueue() as q:
        qml.QubitUnitary(mat, wires=[0, 1])
    tape = qml.tape.QuantumScript.from_queue(q)
    transpiled_tapes, _ = qml.transforms.transpile(
        tape, basis_gates=["U3", "CNOT"], optimization_level=1
    )
    return transpiled_tapes[0]
