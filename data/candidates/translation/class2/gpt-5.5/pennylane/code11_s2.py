# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml


def get_statevector(circuit):
    if isinstance(circuit, qml.QNode):
        tape = circuit.construct((), {})
        if tape is None:
            tape = circuit._tape
        operations = list(tape.operations)

        device_wires = getattr(circuit.device, "wires", None)
        if device_wires is not None and len(device_wires) > 0:
            wires = list(device_wires)
        else:
            wires = list(tape.wires)

    elif hasattr(circuit, "operations"):
        operations = list(circuit.operations)
        wires = list(getattr(circuit, "wires", []))

        if not wires and hasattr(circuit, "num_wires"):
            wires = list(range(circuit.num_wires))

    elif callable(circuit):
        with qml.queuing.AnnotatedQueue() as queue:
            circuit()
        tape = qml.tape.QuantumScript.from_queue(queue)
        operations = list(tape.operations)
        wires = list(tape.wires)

    else:
        operations = list(circuit)
        wires = list(qml.wires.Wires.all_wires([op.wires for op in operations]))

    if len(wires) == 0:
        return qml.numpy.array([1.0 + 0.0j])

    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def state_circuit():
        for op in operations:
            qml.apply(op)
        return qml.state()

    return state_circuit()
