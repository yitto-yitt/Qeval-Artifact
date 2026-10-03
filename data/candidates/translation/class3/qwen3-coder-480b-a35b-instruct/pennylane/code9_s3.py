# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    def circuit(params, wires):
        qml.layer(lambda p, w: qml.templates.BasicEntanglerLayers(p, w), 1, params=params, wires=wires)
    
    # Create the template structure for EfficientSU2 with 3 qubits, 1 rep, barriers
    n_wires = 3
    reps = 1
    
    # For EfficientSU2, we need to define the structure manually since there's no direct equivalent
    def efficient_su2_template(params, wires):
        layer_params = params[0]
        qml.templates.StronglyEntanglingLayers(layer_params, wires=wires)
        
        if True:  # insert_barriers = True
            qml.Barrier(wires=wires)
    
    return efficient_su2_template
