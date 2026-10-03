# EVAL_META: task_id=44, framework=pennylane, class=3
import pennylane as qml

def tensor_circuits():
    def top_circuit():
        qml.PauliX(wires=0)
    
    def bottom_circuit():
        qml.CRY(0.2, wires=[0, 1])
    
    dev = qml.device('default.qubit', wires=3)
    
    @qml.qnode(dev)
    def combined_circuit():
        bottom_circuit()
        top_circuit()
        return qml.state()
    
    # Create the operations separately to match tensor structure
    ops_bottom = [qml.CRY(0.2, wires=[0, 1])]
    ops_top = [qml.PauliX(wires=2)]
    
    # Combine operations with proper wire mapping for tensor product
    all_ops = ops_bottom + ops_top
    
    return all_ops
