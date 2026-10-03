# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    n = num_state_qubits
    if n < 1:
        raise ValueError("num_state_qubits must be at least 1")

    if kind == "full":
        total_qubits = 2 * n + 2
        qubits = cirq.LineQubit.range(total_qubits)
        carry = qubits[0]
        a = qubits[1 : n + 1]
        b = qubits[n + 1 : 2 * n + 1]
        cout = qubits[2 * n + 1]
    elif kind == "half":
        total_qubits = 2 * n + 2
        qubits = cirq.LineQubit.range(total_qubits)
        a = qubits[0:n]
        b = qubits[n : 2 * n]
        cout = qubits[2 * n]
        carry = qubits[2 * n + 1]
    else:
        total_qubits = 2 * n + 1
        qubits = cirq.LineQubit.range(total_qubits)
        a = qubits[0:n]
        b = qubits[n : 2 * n]
        carry = qubits[2 * n]
        cout = None

    def maj(carry_in, b_qubit, a_qubit):
        return [
            cirq.CNOT(a_qubit, b_qubit),
            cirq.CNOT(a_qubit, carry_in),
            cirq.TOFFOLI(carry_in, b_qubit, a_qubit),
        ]

    def uma(carry_in, b_qubit, a_qubit):
        return [
            cirq.TOFFOLI(carry_in, b_qubit, a_qubit),
            cirq.CNOT(a_qubit, carry_in),
            cirq.CNOT(carry_in, b_qubit),
        ]

    circuit = cirq.Circuit()

    circuit.append(maj(carry, b[0], a[0]))

    for i in range(n - 1):
        circuit.append(maj(a[i], b[i + 1], a[i + 1]))

    if kind != "fixed":
        circuit.append(cirq.CNOT(a[n - 1], cout))

    for i in reversed(range(n - 1)):
        circuit.append(uma(a[i], b[i + 1], a[i + 1]))

    circuit.append(uma(carry, b[0], a[0]))

    return circuit