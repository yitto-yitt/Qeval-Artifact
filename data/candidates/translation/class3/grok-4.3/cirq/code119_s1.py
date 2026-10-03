# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == 'full':
        total_qubits = 2 * n + 1
    elif kind == 'half':
        total_qubits = 2 * n
    else:
        total_qubits = 2 * n
    qubits = cirq.LineQubit.range(total_qubits)
    a = qubits[:n]
    b = qubits[n:2 * n]
    anc = qubits[-1] if kind == 'full' else None
    circuit = cirq.Circuit()
    if n == 0:
        return circuit
    if kind == 'full':
        circuit.append(cirq.CNOT(a[0], b[0]))
        circuit.append(cirq.CNOT(b[0], anc))
        circuit.append(cirq.CCX(a[0], anc, b[0]))
        for i in range(1, n):
            circuit.append(cirq.CNOT(a[i], b[i]))
            circuit.append(cirq.CNOT(b[i], b[i - 1]))
            circuit.append(cirq.CCX(a[i], b[i - 1], b[i]))
        circuit.append(cirq.CNOT(b[n - 1], anc))
        for i in range(n - 1, 0, -1):
            circuit.append(cirq.CCX(a[i], b[i - 1], b[i]))
            circuit.append(cirq.CNOT(b[i], b[i - 1]))
            circuit.append(cirq.CNOT(a[i], b[i]))
        circuit.append(cirq.CCX(a[0], anc, b[0]))
        circuit.append(cirq.CNOT(b[0], anc))
        circuit.append(cirq.CNOT(a[0], b[0]))
    elif kind == 'half':
        circuit.append(cirq.CNOT(a[0], b[0]))
        for i in range(1, n):
            circuit.append(cirq.CNOT(a[i], b[i]))
            circuit.append(cirq.CCX(a[i], b[i - 1], b[i]))
        for i in range(n - 1, 0, -1):
            circuit.append(cirq.CCX(a[i], b[i - 1], b[i]))
            circuit.append(cirq.CNOT(a[i], b[i]))
    else:
        for i in range(n):
            circuit.append(cirq.CNOT(a[i], b[i]))
    return circuit
