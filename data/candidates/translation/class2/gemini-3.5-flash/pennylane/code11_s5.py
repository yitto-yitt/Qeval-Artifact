# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.QNode):
        dev = circuit.device
        @qml.qnode(dev)
        def new_circuit():
            circuit.func()
            return qml.state()
        return new_circuit()
    
    if isinstance(circuit, (qml.tape.QuantumTape, qml.tape.QuantumScript)):
        wires = circuit.wires if len(circuit.wires) > 0 else [0]
        dev = qml.device('default.qubit', wires=wires)
        @qml.qnode(dev)
        def new_circuit():
            for op in circuit.operations:
                qml.apply(op)
            return qml.state()
        return new_circuit()

    if callable(circuit):
        with qml.queuing.AnnotatedQueue() as q:
            circuit()
        tape = qml.tape.QuantumScript.from_queue(q)
        wires = tape.wires if len(tape.wires) > 0 else [0]
        dev = qml.device('default.qubit', wires=wires)
        @qml.qnode(dev)
        def new_circuit():
            circuit()
            return qml.state()
        return new_circuit()

    raise TypeError("Unsupported circuit type")
