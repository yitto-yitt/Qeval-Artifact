# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    a = [cirq.NamedQubit(f"a_{i}") for i in range(n)]
    b = [cirq.NamedQubit(f"b_{i}") for i in range(n)]
    
    qubits = []
    qubits.extend(a)
    qubits.extend(b)
    
    cin = None
    cout = None
    
    if kind == 'full':
        cin = cirq.NamedQubit("cin")
        cout = cirq.NamedQubit("cout")
        qubits.append(cin)
        qubits.append(cout)
    elif kind == 'half':
        pass
    elif kind == 'fixed':
        cout = cirq.NamedQubit("cout")
        qubits.append(cout)
        
    qc = cirq.Circuit()
    
    def maj(x, y, z):
        qc.append(cirq.CNOT(z, y))
        qc.append(cirq.CNOT(z, x))
        qc.append(cirq.TOFFOLI(x, y, z))
        
    def uma(x, y, z):
        qc.append(cirq.TOFFOLI(x, y, z))
        qc.append(cirq.CNOT(z, x))
        qc.append(cirq.CNOT(x, y))
        
    if kind == 'full':
        maj(cin, b[0], a[0])
        for i in range(n - 1):
            maj(a[i], b[i+1], a[i+1])
        qc.append(cirq.CNOT(a[-1], cout))
        for i in reversed(range(n - 1)):
            uma(a[i], b[i+1], a[i+1])
        uma(cin, b[0], a[0])
    elif kind == 'half':
        qc.append(cirq.CNOT(a[0], b[0]))
        for i in range(n - 1):
            maj(a[i], b[i+1], a[i+1])
        for i in reversed(range(n - 1)):
            uma(a[i], b[i+1], a[i+1])
        qc.append(cirq.CNOT(a[0], b[0]))
    elif kind == 'fixed':
        qc.append(cirq.CNOT(a[0], b[0]))
        for i in range(n - 1):
            maj(a[i], b[i+1], a[i+1])
        qc.append(cirq.CNOT(a[-1], cout))
        for i in reversed(range(n - 1)):
            uma(a[i], b[i+1], a[i+1])
        qc.append(cirq.CNOT(a[0], b[0]))
        
    return qc
