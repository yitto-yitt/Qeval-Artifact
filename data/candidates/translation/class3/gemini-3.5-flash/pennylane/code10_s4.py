# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_operator():
    dev = qml.device("default.qubit", wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.U3(np.pi, 0, np.pi, wires=0)
        qml.U3(np.pi, 0, np.pi, wires=1)
        return qml.state()
        
    return circuit
