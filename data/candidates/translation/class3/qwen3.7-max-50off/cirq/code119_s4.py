# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    if kind == 'full':
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(i + n) for i in range(n)]
        cin = cirq.LineQubit(2 * n)
        cout = cirq.LineQubit(2 * n + 1)
        qubits = a + b + [cin, cout]
    elif kind == 'half':
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(i + n) for i in range(n)]
        cout = cirq.LineQubit(2 * n)
        qubits = a + b + [cout]
    elif kind == 'fixed':
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(i + n) for i in range(n)]
        qubits = a + b
    else:
        raise ValueError(f"Unknown kind: {kind}")

    circuit = cirq.Circuit()

    def maj(x, y, z):
        circuit.append(cirq.CNOT(z, y))
        circuit.append(cirq.CNOT(z, x))
        circuit.append(cirq.TOFFOLI(x, y, z))

    def uma(x, y, z):
        circuit.append(cirq.TOFFOLI(x, y, z))
        circuit.append(cirq.CNOT(z, x))
        circuit.append(cirq.CNOT(x, y))

    if kind == 'full':
        maj(cin, a[0], b[0])
        for i in range(1, n):
            maj(b[i-1], a[i], b[i])
        
        circuit.append(cirq.CNOT(b[n-1], cout))
        
        for i in range(n-1, 0, -1):
            uma(b[i-1], a[i], b[i])
        uma(cin, a[0], b[0])
        
    elif kind == 'half':
        if n == 1:
            circuit.append(cirq.TOFFOLI(a[0], b[0], cout))
            circuit.append(cirq.CNOT(b[0], a[0]))
        else:
            circuit.append(cirq.TOFFOLI(a[0], b[0], b[1]))
            circuit.append(cirq.CNOT(b[0], a[0]))
            for i in range(1, n):
                maj(b[i-1], a[i], b[i])
            circuit.append(cirq.CNOT(b[n-1], cout))
            for i in range(n-1, 1, -1):
                uma(b[i-1], a[i], b[i])
            circuit.append(cirq.TOFFOLI(a[0], b[0], b[1]))
            circuit.append(cirq.CNOT(b[1], a[1]))
            circuit.append(cirq.CNOT(a[0], b[1]))
            
    elif kind == 'fixed':
        if n == 1:
            circuit.append(cirq.CNOT(b[0], a[0]))
        else:
            circuit.append(cirq.TOFFOLI(a[0], b[0], b[1]))
            circuit.append(cirq.CNOT(b[0], a[0]))
            for i in range(1, n):
                maj(b[i-1], a[i], b[i])
            for i in range(n-1, 1, -1):
                uma(b[i-1], a[i], b[i])
            circuit.append(cirq.TOFFOLI(a[0], b[0], b[1]))
            circuit.append(cirq.CNOT(b[1], a[1]))
            circuit.append(cirq.CNOT(a[0], b[1]))

    return circuit
