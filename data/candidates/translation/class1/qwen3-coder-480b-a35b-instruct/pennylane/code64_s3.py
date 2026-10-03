# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    dev = qml.device('default.qubit', wires=2*n)
    
    @qml.qnode(dev)
    def circuit():
        # Apply Hadamard to first n qubits
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Apply CNOT gates between corresponding qubits in first and second register
        for i in range(n):
            qml.CNOT(wires=[i, n+i])
        
        if "1" in s:
            i = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[i, n+j])
            
            # Apply Hadamard again to first n qubits
            for i in range(n):
                qml.Hadamard(wires=i)
        
        # Measure the first n qubits
        return [qml.sample(qml.PauliZ(i)) for i in range(n)]
    
    # Execute the circuit to ensure it's built properly
    _ = circuit()
    
    # Since PennyLane doesn't have the same circuit representation as Qiskit,
    # we'll create a template-style function that can be used within PennyLane
    def build_circuit():
        qml.template(circuit)
    
    return circuit
