# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.tape.QuantumScript):
        tape = circuit
    else:
        tape = qml.tape.make_qscript(circuit)()
    wires = tape.wires
    dev = qml.device('default.qubit', wires=wires)
    @qml.qnode(dev)
    def qnode():
        for op in tape.operations:
            qml.apply(op)
        return qml.state()
    return qnode()
