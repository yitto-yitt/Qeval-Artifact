# EVAL_META: task_id=38, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    dev = qml.device("default.qubit", wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CRZ(theta, wires=[0, 1])
        qml.Hadamard(wires=1)
        qml.CRY(theta, wires=[1, 0])
        return qml.state()
        
    return circuit
