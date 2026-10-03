# EVAL_META: task_id=52, framework=pennylane, class=1
import pennylane as qml


def send_bits(bitstring):
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        # Create initial entanglement
        qml.Hadamard(wires=0)  # sender
        qml.CNOT(wires=[0, 1])  # sender -> receiver
        
        # Apply operations based on bitstring
        if bitstring[1] == "1":
            qml.PauliZ(wires=0)  # sender
        if bitstring[0] == "1":
            qml.PauliX(wires=0)  # sender
            
        # Disentangle and measure
        qml.CNOT(wires=[0, 1])  # sender -> receiver
        qml.Hadamard(wires=0)   # sender
        
        # Return measurement results (simulate measurements)
        return qml.sample(qml.PauliZ(0)), qml.sample(qml.PauliZ(1))
    
    # Execute the circuit to get results
    result = circuit()
    return circuit  # Return the QNode/circuit definition
