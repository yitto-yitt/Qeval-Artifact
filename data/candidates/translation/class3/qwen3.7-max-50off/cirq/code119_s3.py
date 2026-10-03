# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    a = cirq.LineQubit.range(0, n)
    b = cirq.LineQubit.range(n, 2 * n)
    
    qubits = list(a) + list(b)
    
    cin_q = None
    cout_q = None
    carry_line = None
    
    if kind == 'full':
        cin_q = cirq.LineQubit(2 * n)
        cout_q = cirq.LineQubit(2 * n + 1)
        qubits.extend([cin_q, cout_q])
        carry_line = cin_q
    elif kind == 'half':
        cin_q = cirq.LineQubit(2 * n)
        qubits.append(cin_q)
        carry_line = cin_q
    elif kind == 'fixed':
        cout_q = cirq.LineQubit(2 * n)
        qubits.append(cout_q)
        carry_line = cirq.LineQubit(2 * n + 1)
        qubits.append(carry_line)
        
    circuit = cirq.Circuit()
    
    def maj(x, y, z):
        circuit.append(cirq.CNOT(x, y))
        circuit.append(cirq.CNOT(x, z))
        circuit.append(cirq.TOFFOLI(y, z, x))
        
    def uma(x, y, z):
        circuit.append(cirq.TOFFOLI(y, z, x))
        circuit.append(cirq.CNOT(x, z))
        circuit.append(cirq.CNOT(y, z))
        
    if n > 0:
        maj(carry_line, b[0], a[0])
        for i in range(1, n):
            maj(carry_line, b[i], a[i])
            
        if cout_q is not None:
            circuit.append(cirq.CNOT(carry_line, cout_q))
            
        for i in range(n - 1, 0, -1):
            uma(carry_line, b[i], a[i])
        uma(carry_line, b[0], a[0])
        
    return circuit
