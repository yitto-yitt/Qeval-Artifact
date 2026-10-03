# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    with qml.tape.QuantumTape() as tape:
        circuit()
    wires = set()
    for op in tape.operations:
        wires.update(op.wires)
    if not wires:
        dev = qml.device('default.qubit', wires=0)
    else:
        num_wires = max(wires) + 1
        dev = qml.device('default.qubit', wires=num_wires)
    @qml.qnode(dev)
    def circ():
        circuit()
        return qml.state()
    return circ()
