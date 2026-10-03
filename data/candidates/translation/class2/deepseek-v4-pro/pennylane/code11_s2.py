# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml


def get_statevector(circuit):
    tape = getattr(circuit, "qtape", circuit)
    wires = tape.wires if len(tape.wires) > 0 else qml.wires.Wires([0])
    dev = qml.device("default.qubit", wires=wires)
    state_tape = qml.tape.QuantumScript(list(tape.operations), [qml.state()])
    return qml.execute([state_tape], dev, gradient_fn=None)[0]
