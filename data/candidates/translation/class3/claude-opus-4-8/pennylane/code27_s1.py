# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml


def apply_op_back():
    ops = []
    ops.append(qml.Hadamard(wires=0))
    ops.append(qml.CNOT(wires=[0, 1]))
    ops.append(qml.Hadamard(wires=0))

    def circuit():
        for op in ops:
            qml.apply(op)
        return qml.state()

    dev = qml.device("default.qubit", wires=3)
    qnode = qml.QNode(circuit, dev)
    tape = qml.workflow.construct_tape(qnode)()
    return tape
