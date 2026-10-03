# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.tape.QuantumTape):
        wires = circuit.wires
        num_wires = len(wires)
    elif callable(circuit):
        tape = qml.workflow.construct_tape(circuit)()
        wires = tape.wires
        num_wires = len(wires)
        circuit = tape
    else:
        raise TypeError("Unsupported circuit type")

    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def _circuit():
        for op in circuit.operations:
            qml.apply(op)
        return qml.state()

    return _circuit()
