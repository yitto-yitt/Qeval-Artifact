# EVAL_META: task_id=71, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_csx01_h1():
    dev = qml.device("default.qubit", wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.ctrl(qml.SX(wires=1), control=0)
        qml.Hadamard(wires=1)
        return qml.state()
        
    return circuit
