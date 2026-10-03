# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.QNode):
        tape = qml.workflow.construct_tape(circuit)()
        wires = circuit.device.wires
        if wires is None:
            wires = tape.wires
    elif isinstance(circuit, qml.tape.QuantumScript):
        tape = circuit
        wires = tape.wires
    else:
        tape = qml.tape.make_qscript(circuit)()
        wires = tape.wires

    state_tape = qml.tape.QuantumScript(
        operations=tape.operations,
        measurements=[qml.state()],
        shots=None,
    )
    device = qml.device("default.qubit", wires=wires, shots=None)
    return qml.execute((state_tape,), device, diff_method=None)[0]
