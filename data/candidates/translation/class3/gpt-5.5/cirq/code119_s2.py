# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    n = num_state_qubits
    if n < 1:
        raise ValueError("The number of state qubits must be at least 1.")

    if kind == "full":
        num_qubits = 2 * n + 2
        qubits = cirq.LineQubit.range(num_qubits)
        carry = qubits[0]
        a = list(qubits[1 : n + 1])
        b = list(qubits[n + 1 : 2 * n + 1])
        cout = qubits[2 * n + 1]
    elif kind == "half":
        num_qubits = 2 * n + 2
        qubits = cirq.LineQubit.range(num_qubits)
        a = list(qubits[0:n])
        b = list(qubits[n : 2 * n])
        cout = qubits[2 * n]
        carry = qubits[2 * n + 1]
    else:
        num_qubits = 2 * n + 1
        qubits = cirq.LineQubit.range(num_qubits)
        a = list(qubits[0:n])
        b = list(qubits[n : 2 * n])
        cout = None
        carry = qubits[2 * n]

    circuit = cirq.Circuit()

    def maj(x, y, z):
        circuit.append(cirq.CNOT(x, y))
        circuit.append(cirq.CNOT(x, z))
        circuit.append(cirq.CCX(z, y, x))

    def uma(x, y, z):
        circuit.append(cirq.CCX(z, y, x))
        circuit.append(cirq.CNOT(x, z))
        circuit.append(cirq.CNOT(z, y))

    maj(a[0], b[0], carry)

    for i in range(1, n):
        maj(a[i], b[i], a[i - 1])

    if kind in ("full", "half"):
        circuit.append(cirq.CNOT(a[-1], cout))

    for i in range(n - 1, 0, -1):
        uma(a[i], b[i], a[i - 1])

    uma(a[0], b[0], carry)

    return circuit
