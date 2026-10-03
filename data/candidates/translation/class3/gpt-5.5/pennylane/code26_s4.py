# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml


def bell_dag():
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
    ]
    measurements = [qml.sample(wires=0)]
    tape = qml.tape.QuantumScript(ops, measurements)
    return tape.graph
