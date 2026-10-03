# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    def circuit(weights):
        idx = 0
        # Layer 0
        for i in range(3):
            qml.RY(weights[idx], wires=i)
            qml.RZ(weights[idx+1], wires=i)
            idx += 2
        
        qml.Barrier(wires=[0, 1, 2])
        
        # Entanglement layer (circular CX)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 0])
        
        qml.Barrier(wires=[0, 1, 2])
        
        # Layer 1
        for i in range(3):
            qml.RY(weights[idx], wires=i)
            qml.RZ(weights[idx+1], wires=i)
            idx += 2
            
    return circuit
