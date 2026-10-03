# EVAL_META: task_id=52, framework=pennylane, class=1
import pennylane as qml


def send_bits(bitstring):
    dev = qml.device('default.qubit', wires=2, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        # Create initial entanglement between sender and receiver
        qml.Hadamard(wires=0)  # sender
        qml.CNOT(wires=[0, 1])  # entangle sender and receiver
        
        # Apply operations based on the bits to send
        if bitstring[1] == "1":
            qml.PauliZ(wires=0)  # sender
        if bitstring[0] == "1":
            qml.PauliX(wires=0)  # sender
            
        # Disentangle and measure
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
        
        # Measure both qubits
        m1 = qml.measure(wires=0)
        m2 = qml.measure(wires=1)
        
        return m1, m2
    
    return circuit
