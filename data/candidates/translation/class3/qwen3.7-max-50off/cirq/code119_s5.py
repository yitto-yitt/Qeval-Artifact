# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    if kind == 'full':
        cin = cirq.LineQubit(0)
        a = [cirq.LineQubit(i + 1) for i in range(n)]
        b = [cirq.LineQubit(i + 1 + n) for i in range(n)]
        cout = cirq.LineQubit(2 * n + 1)
    elif kind == 'half':
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(i + n) for i in range(n)]
        cout = cirq.LineQubit(2 * n)
        cin = None
    elif kind == 'fixed':
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(i + n) for i in range(n)]
        cout = None
        cin = None
    else:
        raise ValueError(f"Unknown kind: {kind}")

    circuit = cirq.Circuit()
    
    # Forward pass (MAJ operations)
    for i in range(n):
        if i == 0 and kind != 'full':
            c_q = None
        else:
            c_q = cin if i == 0 else a[i - 1]
            
        if c_q is not None:
            circuit.append(cirq.CNOT(a[i], b[i]))
            circuit.append(cirq.CNOT(a[i], c_q))
            circuit.append(cirq.CCX(c_q, b[i], a[i]))
        else:
            circuit.append(cirq.CNOT(a[i], b[i]))
            
    # Carry out
    if kind in ['full', 'half']:
        circuit.append(cirq.CNOT(a[n - 1], cout))
        
    # Backward pass (UMA operations)
    for i in range(n - 1, -1, -1):
        if i == 0 and kind != 'full':
            c_q = None
        else:
            c_q = cin if i == 0 else a[i - 1]
            
        if c_q is not None:
            circuit.append(cirq.CCX(c_q, b[i], a[i]))
            circuit.append(cirq.CNOT(a[i], c_q))
            circuit.append(cirq.CNOT(c_q, b[i]))

    return circuit
