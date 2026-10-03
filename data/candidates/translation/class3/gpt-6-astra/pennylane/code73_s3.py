# EVAL_META: task_id=73, framework=pennylane, class=3
import pennylane as qml


def x_measurement(circuit, qubit, clbit):
    with qml.QueuingManager.stop_recording():
        hadamard = qml.Hadamard(wires=qubit)
        result = qml.measure(wires=qubit)
        measurement = result.measurements[0]
        measurement._id = str(clbit)

    if isinstance(circuit, qml.tape.QuantumScript):
        circuit._ops.extend([hadamard, measurement])
        for key in ("graph", "specs", "wires", "num_wires", "par_info"):
            circuit.__dict__.pop(key, None)
    else:
        circuit.append(hadamard)
        circuit.append(measurement)
