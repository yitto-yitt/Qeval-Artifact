# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    a = cirq.LineQubit.range(0, n)
    b = cirq.LineQubit.range(n, 2*n)
    
    if kind == 'full':
        cin_q = cirq.LineQubit(2*n)
        cout_q = cirq.LineQubit(2*n+1)
    elif kind == 'half':
        cin_q = cirq.NamedQubit("_cin")
        cout_q = cirq.LineQubit(2*n)
    elif kind == 'fixed':
        cin_q = cirq.NamedQubit("_cin")
        cout_q = cirq.NamedQubit("_cout")
    else:
        raise ValueError(f"Unknown kind: {kind}")

    circuit = cirq.Circuit()

    def maj(c, x, y):
        circuit.append(cirq.CX(c, y))
        circuit.append(cirq.CX(c, x))
        circuit.append(cirq.CCX(x, y, c))

    def uma(c, x, y):
        circuit.append(cirq.CCX(x, y, c))
        circuit.append(cirq.CX(c, x))
        circuit.append(cirq.CX(x, y))

    maj(cin_q, a[0], b[0])
    for i in range(1, n):
        maj(a[i-1], a[i], b[i])
        
    if kind != 'fixed':
        circuit.append(cirq.CX(a[-1], cout_q))
    
    for i in range(n-1, 0, -1):
        uma(a[i-1], a[i], b[i])
    uma(cin_q, a[0], b[0])

    return circuit
