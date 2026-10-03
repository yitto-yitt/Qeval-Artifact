# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml


def bell_dag():
    with qml.queuing.AnnotatedQueue() as q:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.measure(0)
    tape = qml.tape.QuantumScript.from_queue(q)
    return qml.commutation_dag(tape)
