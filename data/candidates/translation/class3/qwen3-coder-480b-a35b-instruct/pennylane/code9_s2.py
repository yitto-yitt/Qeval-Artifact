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
            # Apply rotation gates
            for i, wire in enumerate(wires):
                qml.Rot(*params[0][layer][i], wires=wire)
            
            # Apply entangling layers with barriers
            for i in range(len(wires) - 1):
                qml.CNOT(wires=[wires[i], wires[i+1]])
            if reps > 0:  # Add barrier after each rep except the last one
                qml.Barrier(wires=wires)
    
    return efficient_su2_template
