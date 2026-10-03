# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    dev = qml.device("default.qubit", wires=5)
    
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
    
    qnode_full = qml.QNode(circuit, dev)
    qnode_limited = qml.QNode(circuit, dev)
    return qnode_full, qnode_limited
