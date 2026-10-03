# EVAL_META: task_id=89, framework=pennylane, class=3

import pennylane as qml

def create_controlled_hgate():
    dev = qml.device('default.qubit', wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.ctrl(qml.Hadamard, control=[0, 1])(wires=2)
        return qml.state()

    return circuit
