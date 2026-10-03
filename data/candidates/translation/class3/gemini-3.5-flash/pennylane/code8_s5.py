# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    dev = qml.device("default.qubit", wires=1)
    
    @qml.qnode(dev)
    def circuit(theta=None):
        val = value if value is not None else theta
        qml.RX(val, wires=0)
        return qml.state()
        
    return circuit
