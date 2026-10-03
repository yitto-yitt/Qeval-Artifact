# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if num_state_qubits < 1:
        raise ValueError("The number of state qubits must be at least 1.")

    n = num_state_qubits
    has_carry_out = kind in ("full", "half")
    qubits = cirq.LineQubit.range(2 * n + 1 + int(has_carry_out))

    if kind == "full":
        carry_in = qubits[0]
        a = qubits[1:n + 1]
        b = qubits[n + 1:2 * n + 1]
        carry_out = qubits[2 * n + 1]
    else:
        a = qubits[:n]
        b = qubits[n:2 * n]
        carry_out = qubits[2 * n] if has_carry_out else None
        carry_in = qubits[-1]

    circuit = cirq.Circuit()

    for i in range(n):
        carry = carry_in if i == 0 else a[i - 1]
        circuit.append(cirq.CNOT(a[i], b[i]))
        circuit.append(cirq.CNOT(a[i], carry))
        circuit.append(cirq.TOFFOLI(carry, b[i], a[i]))

    if has_carry_out:
        circuit.append(cirq.CNOT(a[-1], carry_out))

    for i in reversed(range(n)):
        carry = carry_in if i == 0 else a[i - 1]
        circuit.append(cirq.TOFFOLI(carry, b[i], a[i]))
        circuit.append(cirq.CNOT(a[i], carry))
        circuit.append(cirq.CNOT(carry, b[i]))

    return circuit
