# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    dev = qml.device("default.qubit", wires=3)
    
    @qml.qnode(dev)
    def circuit(weights):
        # weights shape: (2, 3, 2)
        # SU2 layer 0
        for i in range(3):
            qml.RY(weights[0][i][0], wires=i)
            qml.RZ(weights[0][i][1], wires=i)
            
        qml.Barrier(wires=[0, 1, 2])
        
        # Entanglement layer (reverse_linear)
        qml.CNOT(wires=[2, 1])
        qml.CNOT(wires=[1, 0])
        
        qml.Barrier(wires=[0, 1, 2])
        
        # SU2 layer 1
        for i in range(3):
            qml.RY(weights[1][i][0], wires=i)
            qml.RZ(weights[1][i][1], wires=i)
            
        return qml.state()
        
    return circuit
