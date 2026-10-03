# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def decompose_unitary(unitary):
    with qml.queuing.AnnotatedQueue() as q:
        qml.QubitUnitary(unitary, wires=[0, 1])
    tape = qml.tape.QuantumScript.from_queue(q)
    return tape.expand()
