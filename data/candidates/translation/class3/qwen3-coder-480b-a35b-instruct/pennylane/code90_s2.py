# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    def custom_operation(wires):
        qml.PauliX(wires=wires[0])
        qml.Hadamard(wires=wires[1])
    
    def controlled_custom_operation(wires):
        qml.ctrl(custom_operation, control=[wires[0], wires[3]])(wires=[wires[1], wires[2]])
    
    dev = qml.device('default.qubit', wires=4)
    
    @qml.qnode(dev)
    def circuit():
        controlled_custom_operation(wires=[0, 1, 2, 3])
        return qml.state()
    
    # Create the operation as a template
    def template():
        qml.ctrl(lambda wires: (qml.PauliX(wires[0]), qml.Hadamard(wires[1])), control=[0, 3])(wires=[1, 2])
    
    # Return the operation that can be used in a circuit
    return template
