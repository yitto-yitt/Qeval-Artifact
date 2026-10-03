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
            
        # Decode operations
        qml.CNOT(wires=[0, 1])  # sender -> receiver
        qml.Hadamard(wires=0)   # sender
        
        # Measure both qubits
        m0 = qml.measure(wires=0)
        m1 = qml.measure(wires=1)
        
        return m0, m1
    
    return circuit()
