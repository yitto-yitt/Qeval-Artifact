# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'full':
        total_qubits = 2 * num_state_qubits + 2
    elif kind == 'half':
        total_qubits = 2 * num_state_qubits + 1
    else:
        total_qubits = 2 * num_state_qubits
    qubits = cirq.LineQubit.range(total_qubits)
    circuit = cirq.Circuit()
    a = qubits[:num_state_qubits]
    b = qubits[num_state_qubits:2 * num_state_qubits]
    if kind == 'full':
        carry_in = qubits[2 * num_state_qubits]
        carry_out = qubits[2 * num_state_qubits + 1]
        c = carry_in
        for i in range(num_state_qubits):
            circuit.append(cirq.CCX(a[i], b[i], c))
            circuit.append(cirq.CNOT(a[i], b[i]))
            if i < num_state_qubits - 1:
                next_carry = qubits[2 * num_state_qubits + 1] if i == num_state_qubits - 2 else cirq.NamedQubit(f'carry_{i}')
                circuit.append(cirq.CCX(b[i], c, next_carry))
                c = next_carry
        circuit.append(cirq.CNOT(a[-1], carry_out))
    elif kind == 'half':
        c = cirq.NamedQubit('carry')
        for i in range(num_state_qubits):
            circuit.append(cirq.CCX(a[i], b[i], c))
            circuit.append(cirq.CNOT(a[i], b[i]))
    else:
        for i in range(num_state_qubits):
            circuit.append(cirq.CNOT(a[i], b[i]))
    return circuit
