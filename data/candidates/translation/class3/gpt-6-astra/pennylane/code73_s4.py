# EVAL_META: task_id=73, framework=pennylane, class=3
import pennylane as qml


def x_measurement(circuit, qubit, clbit):
    with qml.QueuingManager.stop_recording():
        hadamard = qml.Hadamard(wires=qubit)
        outcome = qml.measure(wires=qubit)
        measurement = outcome.measurements[0]
        measurement._id = str(clbit)

    if isinstance(circuit, qml.tape.QuantumScript):
        circuit.operations.extend([hadamard, measurement])
        circuit._graph = None
        circuit._specs = None
    else:
        circuit.extend([hadamard, measurement])
