# EVAL_META: task_id=70, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    dev = qml.device("default.qubit", wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CSWAP(wires=[0, 1, 2])
        qml.Hadamard(wires=1)
        qml.adjoint(qml.ctrl(qml.S, control=1))(wires=0)
        return qml.state()
        
    return circuit
