# EVAL_META: task_id=49, framework=pennylane, class=3
import pennylane as qml

def simple_elitzur_vaidman():
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
    
    dev = qml.device('default.qubit', wires=2)
    qnode = qml.QNode(circuit, dev)
    return qnode
