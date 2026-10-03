# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def decompose_unitary(unitary):
    unitary = np.asarray(unitary, dtype=complex)
    with qml.queuing.AnnotatedQueue() as q:
        qml.QubitUnitary(unitary, wires=[0, 1])
    tape = qml.tape.QuantumScript.from_queue(q)
    decomposed_tape = qml.transforms.unitary_to_rot(tape.expand(depth=10))
    return decomposed_tape
