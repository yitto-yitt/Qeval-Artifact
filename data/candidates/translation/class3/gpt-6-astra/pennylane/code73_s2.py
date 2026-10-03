# EVAL_META: task_id=73, framework=pennylane, class=3
import pennylane as qml


def x_measurement(circuit, qubit, clbit):
    with qml.QueuingManager.stop_recording():
        hadamard = qml.Hadamard(wires=qubit)
        result = qml.measure(wires=qubit)
        measurement = result.measurements[0]
        measurement._id = str(clbit)

    if isinstance(circuit, qml.tape.QuantumScript):
        circuit.operations.extend([hadamard, measurement])
        circuit._graph = None
        circuit._specs = None
        circuit._trainable_params = None
        for name in ("par_info", "wires", "num_wires", "batch_size", "observables"):
            circuit.__dict__.pop(name, None)
    else:
        circuit.append(hadamard)
        circuit.append(measurement)
