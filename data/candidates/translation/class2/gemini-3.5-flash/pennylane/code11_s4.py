# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.tape.QuantumScript):
        tape = circuit
    elif isinstance(circuit, qml.QNode):
        tape = qml.workflow.construct_tape(circuit)()
    elif callable(circuit):
        tape = qml.workflow.construct_tape(circuit)()
    else:
        tape = circuit

    wires = list(tape.wires) if len(tape.wires) > 0 else [0]
    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def state_circuit():
        for op in tape.operations:
            qml.apply(op)
        return qml.state()

    return state_circuit()
