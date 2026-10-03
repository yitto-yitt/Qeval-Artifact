# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    dev = qml.device("default.qubit", wires=4)
    
    @qml.qnode(dev)
    def circuit():
        qml.ctrl(qml.SX(3), control=[0, 1, 2])
        return qml.state()
        
    return circuit
