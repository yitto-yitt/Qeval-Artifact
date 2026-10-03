# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml


def bell_dag():
    tape = qml.tape.QuantumScript(
        [qml.Hadamard(0), qml.CNOT([0, 1])],
        [qml.measure(0)]
    )
    return tape
