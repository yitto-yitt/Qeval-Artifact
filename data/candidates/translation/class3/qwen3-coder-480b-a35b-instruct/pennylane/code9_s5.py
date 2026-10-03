# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    def circuit(params, wires):
        qml.StronglyEntanglingLayers(weights=params, wires=wires)
    
    # Create the template structure similar to EfficientSU2
    def efficient_su2_template(wires, reps=1):
        n_wires = len(wires)
        params = [[[[0.0 for _ in range(3)] for _ in range(n_wires)] for _ in range(reps)]]
        
        for layer in range(reps):
            # Apply rotation layers
            for wire in wires:
                qml.RX(0.0, wires=wire)
                qml.RY(0.0, wires=wire)
                qml.RZ(0.0, wires=wire)
            
            # Apply entangling layers with barriers
            for i in range(n_wires):
                for j in range(i + 1, n_wires):
                    qml.CNOT(wires=[wires[i], wires[j]])
            
            if reps > 0:  # Add barrier after each layer if needed
                qml.Barrier(wires=wires)
    
    # Since PennyLane doesn't have EfficientSU2 directly, we return the template function
    return efficient_su2_template
