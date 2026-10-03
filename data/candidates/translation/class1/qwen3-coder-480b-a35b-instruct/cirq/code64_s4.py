# EVAL_META: task_id=64, framework=cirq, class=1
import cirq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    qubits1 = [cirq.LineQubit(i) for i in range(n)]
    qubits2 = [cirq.LineQubit(i + n) for i in range(n)]
    
    circuit = cirq.Circuit()
    
    # Apply Hadamard to first register
    circuit.append(cirq.H.on_each(qubits1))
    
    # Add barrier equivalent (just continue with operations)
    # CX gate between qubits1 and qubits2
    for i in range(n):
        circuit.append(cirq.CNOT(qubits1[i], qubits2[i]))
    
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.append(cirq.CNOT(qubits1[i], qubits2[j]))
        
        # Add barrier equivalent
        # Apply Hadamard to first register again
        circuit.append(cirq.H.on_each(qubits1))
    
    # Measure the first register
    circuit.append(cirq.measure(*qubits1, key='c'))
    
    return circuit
