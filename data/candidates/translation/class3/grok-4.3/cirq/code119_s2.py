# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'full':
        n = num_state_qubits
        qubits = cirq.LineQubit.range(2 * n + 2)
        a = qubits[:n]
        b = qubits[n:2 * n]
        carry_in = qubits[2 * n]
        carry_out = qubits[2 * n + 1]
    elif kind == 'half':
        n = num_state_qubits
        qubits = cirq.LineQubit.range(2 * n + 1)
        a = qubits[:n]
        b = qubits[n:2 * n]
        carry_out = qubits[2 * n]
        carry_in = None
    else:
        n = num_state_qubits
        qubits = cirq.LineQubit.range(2 * n + 1)
        a = qubits[:n]
        b = qubits[n:2 * n]
        carry_out = qubits[2 * n]
        carry_in = None
    circuit = cirq.Circuit()
    if kind == 'full' and carry_in is not None:
        circuit.append(cirq.CNOT(carry_in, b[0]))
    for i in range(n):
        if i == 0:
            circuit.append(cirq.CCNOT(a[i], b[i], carry_out))
        else:
            circuit.append(cirq.CCNOT(a[i], b[i], carry_out))
            circuit.append(cirq.CNOT(carry_out, b[i]))
            circuit.append(cirq.CCNOT(a[i], b[i], carry_out))
    for i in range(n - 1, -1, -1):
        if i > 0:
            circuit.append(cirq.CNOT(carry_out, b[i]))
            circuit.append(cirq.CCNOT(a[i], b[i], carry_out))
    if kind == 'full' and carry_in is not None:
        circuit.append(cirq.CNOT(carry_in, b[0]))
    return circuit
