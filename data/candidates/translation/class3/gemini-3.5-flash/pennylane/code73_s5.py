# EVAL_META: task_id=73, framework=pennylane, class=3
import pennylane as qml

def x_measurement(circuit, qubit, clbit):
    if isinstance(circuit, list):
        circuit.append(qml.Hadamard(wires=qubit))
        circuit.append(qml.measure(wires=qubit))
    else:
        qml.Hadamard(wires=qubit)
        qml.measure(wires=qubit)
