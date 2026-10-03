# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def get_statevector(circuit):
    wires = list(circuit.wires)
    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def _state():
        qml.apply(circuit)
        return qml.state()

    return _state()
