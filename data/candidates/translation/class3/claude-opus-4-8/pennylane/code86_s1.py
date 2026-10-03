# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
        return qml.state()

    dev = qml.device("default.qubit", wires=5)

    full_block = qml.QNode(circuit, dev)
    limited_block = qml.QNode(circuit, dev)

    return full_block, limited_block
