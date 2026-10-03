# EVAL_META: task_id=73, framework=pennylane, class=3
import pennylane as qml

def x_measurement(circuit, qubit, clbit):
    qml.Hadamard(wires=qubit)
    qml.measure(wires=qubit)
