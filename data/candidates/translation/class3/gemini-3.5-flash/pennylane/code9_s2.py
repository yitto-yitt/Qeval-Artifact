# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    dev = qml.device("default.qubit", wires=3)
    
    @qml.qnode(dev)
    def circuit(weights):
        # weights should be a 1D array of 12 parameters
        idx = 0
        # Layer 0 Rotations
        for i in range(3):
            qml.RY(weights[idx], wires=i)
            qml.RZ(weights[idx+1], wires=i)
            idx += 2
            
        qml.Barrier(wires=[0, 1, 2])
        
        # Entanglement (reverse_linear)
        qml.CNOT(wires=[2, 1])
        qml.CNOT(wires=[1, 0])
        
        qml.Barrier(wires=[0, 1, 2])
        
        # Layer 1 Rotations
        for i in range(3):
            qml.RY(weights[idx], wires=i)
            qml.RZ(weights[idx+1], wires=i)
            idx += 2
            
        return qml.state()
        
    return circuit
