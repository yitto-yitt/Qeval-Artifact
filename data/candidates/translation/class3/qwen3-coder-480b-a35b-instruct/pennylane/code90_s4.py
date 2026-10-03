# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    def custom_operation(wires):
        qml.PauliX(wires=wires[0])
        qml.Hadamard(wires=wires[1])
    
    dev = qml.device('default.qubit', wires=4)
    
    @qml.qnode(dev)
    def circuit():
        # Apply the custom operation as a controlled operation
        # Using qml.ctrl to apply the custom operation with control qubits
        qml.ctrl(custom_operation, control=[0, 3])(wires=[1, 2])
        return qml.state()
    
    # We need to return the tape containing the operations
    tape = circuit.qtape
    
    # Create a new device and apply the operations to get the circuit representation
    dev2 = qml.device('default.qubit', wires=4)
    
    @qml.qnode(dev2)
    def build_circuit():
        qml.ctrl(custom_operation, control=[0, 3])(wires=[1, 2])
        return qml.state()
    
    # Execute once to build the tape
    build_circuit()
    
    # Return the tape which represents the circuit
    return build_circuit.qtape
