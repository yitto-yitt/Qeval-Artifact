# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_efficientSU2():
    weights = np.zeros((2, 3, 2))
    with qml.queuing.AnnotatedQueue() as q:
        qml.EfficientSU2(weights, wires=range(3), reps=1)
    return qml.tape.QuantumScript.from_queue(q)
