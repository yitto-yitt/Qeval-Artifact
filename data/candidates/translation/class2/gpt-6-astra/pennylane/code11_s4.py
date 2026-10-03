# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    wires = None
    if isinstance(circuit, qml.QNode):
        tape = circuit.construct((), {})
        wires = circuit.device.wires
    elif isinstance(circuit, qml.tape.QuantumScript):
        tape = circuit
    elif callable(circuit):
        tape = qml.tape.make_qscript(circuit)()
    elif isinstance(circuit, qml.operation.Operator):
        tape = qml.tape.QuantumScript([circuit])
    else:
        tape = qml.tape.QuantumScript(list(circuit))

    if wires is None:
        wires = tape.wires

    device = qml.device("default.qubit", wires=wires, shots=None)
    state_tape = qml.tape.QuantumScript(
        operations=tape.operations,
        measurements=[qml.state()],
        shots=None,
    )
    return qml.execute((state_tape,), device, diff_method=None)[0]
