# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    def maj(circuit, c, b, a):
        circuit.append(cirq.CNOT(a, b))
        circuit.append(cirq.CNOT(a, c))
        circuit.append(cirq.TOFFOLI(b, c, a))

    def uma(circuit, c, b, a):
        circuit.append(cirq.TOFFOLI(b, c, a))
        circuit.append(cirq.CNOT(a, c))
        circuit.append(cirq.CNOT(c, b))

    circuit = cirq.Circuit()
    
    if kind in ['full', 'half']:
        num_qubits = 2 * num_state_qubits + 2
        qubits = cirq.LineQubit.range(num_qubits)
        cin = qubits[0]
        a = qubits[1 : num_state_qubits + 1]
        b = qubits[num_state_qubits + 1 : 2 * num_state_qubits + 1]
        cout = qubits[2 * num_state_qubits + 1]

        if num_state_qubits > 0:
            maj(circuit, cin, b[0], a[0])
            for i in range(1, num_state_qubits):
                maj(circuit, a[i - 1], b[i], a[i])

            circuit.append(cirq.CNOT(a[-1], cout))

            for i in reversed(range(1, num_state_qubits)):
                uma(circuit, a[i - 1], b[i], a[i])
            uma(circuit, cin, b[0], a[0])

    elif kind == 'fixed':
        num_qubits = 2 * num_state_qubits + 1
        qubits = cirq.LineQubit.range(num_qubits)
        cin = qubits[0]
        a = qubits[1 : num_state_qubits + 1]
        b = qubits[num_state_qubits + 1 : 2 * num_state_qubits + 1]

        if num_state_qubits > 1:
            maj(circuit, cin, b[0], a[0])
            for i in range(1, num_state_qubits - 1):
                maj(circuit, a[i - 1], b[i], a[i])

            circuit.append(cirq.CNOT(a[-2], b[-1]))
            circuit.append(cirq.CNOT(a[-1], b[-1]))

            for i in reversed(range(1, num_state_qubits - 1)):
                uma(circuit, a[i - 1], b[i], a[i])
            uma(circuit, cin, b[0], a[0])
        elif num_state_qubits == 1:
            circuit.append(cirq.CNOT(cin, b[0]))
            circuit.append(cirq.CNOT(a[0], b[0]))

    return circuit
