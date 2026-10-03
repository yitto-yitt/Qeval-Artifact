# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.tape.QuantumTape):
        wires = circuit.wires
        num_wires = len(wires)
    elif isinstance(circuit, (list, tuple)):
        num_wires = len(set(w for op in circuit for w in op.wires))
        circuit = qml.tape.QuantumTape(circuit)
        wires = circuit.wires
    else:
        num_wires = len(circuit.wires) if hasattr(circuit, "wires") else None

    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def qnode():
        for op in circuit.operations:
            qml.apply(op)
        return qml.state()

    return qnode()
