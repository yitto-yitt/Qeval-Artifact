# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    dev = qml.device("default.qubit", wires=4)
    
    @qml.qnode(dev)
    def circuit():
        def custom_gate():
            qml.PauliX(wires=1)
            qml.Hadamard(wires=2)
        qml.ctrl(custom_gate, control=[0, 3])()
        return qml.state()
        
    return circuit
