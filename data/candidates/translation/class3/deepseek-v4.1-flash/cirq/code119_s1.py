# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'full':
        num_qubits = 2 * num_state_qubits + 2
    elif kind in ('half', 'fixed'):
        num_qubits = 2 * num_state_qubits + 1
    else:
        num_qubits = 2 * num_state_qubits + 1
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    a = qubits[:num_state_qubits]
    b = qubits[num_state_qubits:2 * num_state_qubits]
    if kind == 'full':
        carry_in = qubits[2 * num_state_qubits]
        carry_out = qubits[2 * num_state_qubits + 1]
        anc = [carry_in] + [cirq.NamedQubit(f'carry_{i}') for i in range(num_state_qubits - 1)] + [carry_out]
    else:
        anc = [cirq.NamedQubit(f'carry_{i}') for i in range(num_state_qubits)]
    for i in range(num_state_qubits):
        if i == 0:
            if kind == 'full':
                circuit.append(cirq.CX(carry_in, b[0]))
            circuit.append(cirq.CX(a[0], b[0]))
        else:
            circuit.append(cirq.CCX(a[i - 1], b[i - 1], anc[i]))
            circuit.append(cirq.CCX(anc[i], b[i], a[i - 1]))
            circuit.append(cirq.CX(a[i], b[i]))
    for i in range(num_state_qubits - 2, -1, -1):
        circuit.append(cirq.CCX(anc[i + 1], b[i + 1], a[i]))
        circuit.append(cirq.CCX(a[i], b[i], anc[i + 1]))
        circuit.append(cirq.CX(a[i], b[i]))
    if kind == 'full':
        circuit.append(cirq.CX(carry_in, b[0]))
        circuit.append(cirq.CX(a[0], b[0]))
    return circuit
