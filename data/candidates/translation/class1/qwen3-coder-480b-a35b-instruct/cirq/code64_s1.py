# EVAL_META: task_id=64, framework=cirq, class=1
import cirq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    # Create qubits
    q_reg1 = [cirq.LineQubit(i) for i in range(n)]
    q_reg2 = [cirq.LineQubit(i + n) for i in range(n)]
    
    # Create circuit
    circuit = cirq.Circuit()
    
    # Apply Hadamard gates to first register
    circuit.append(cirq.H.on_each(*q_reg1))
    
    # Add barrier (in Cirq we use moment annotations or just separate operations)
    circuit.append(cirq.Moment())
    
    # Apply CX gates between registers
    for i in range(n):
        circuit.append(cirq.CNOT(q_reg1[i], q_reg2[i]))
    
    # If there's a '1' in s, apply additional CX gates
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.append(cirq.CNOT(q_reg1[i], q_reg2[j]))
        
        # Add barrier
        circuit.append(cirq.Moment())
        
        # Apply Hadamard gates to first register again
        circuit.append(cirq.H.on_each(*q_reg1))
    
    # Measurements (we don't have classical registers in the same way in Cirq,
    # but we can measure to key names)
    circuit.append(cirq.measure(*q_reg1, key='c'))
    
    return circuit
