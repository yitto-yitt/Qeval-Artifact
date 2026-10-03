# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def get_statevector(circuit):
    if isinstance(circuit, qml.tape.QuantumTape):
        wires = circuit.wires
        num_wires = len(wires)
    else:
        num_wires = None

    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def _circuit():
        for op in circuit.operations:
            qml.apply(op)
        return qml.state()

    return _circuit()
