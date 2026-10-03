# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    dev = qml.device("default.qubit", wires=3)
    
    @qml.qnode(dev)
    def circuit(weights):
        qml.EfficientSU2(weights, wires=range(3))
        return qml.state()
        
    return circuit
