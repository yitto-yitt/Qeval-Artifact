# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if num_state_qubits < 1:
        raise ValueError("The number of state qubits must be at least 1.")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'.")

    n = num_state_qubits
    offset = 1 if kind == "full" else 0
    a = list(range(offset, offset + n))
    b = list(range(offset + n, offset + 2 * n))
    carry = 0 if kind == "full" else 2 * n + (kind == "half")
    carry_out = offset + 2 * n if kind != "fixed" else None

    operations = []

    def majority(x, y, z):
        operations.append(qml.CNOT(wires=[x, y]))
        operations.append(qml.CNOT(wires=[x, z]))
        operations.append(qml.Toffoli(wires=[z, y, x]))

    def unmajority_add(x, y, z):
        operations.append(qml.Toffoli(wires=[z, y, x]))
        operations.append(qml.CNOT(wires=[x, z]))
        operations.append(qml.CNOT(wires=[z, y]))

    majority(a[0], b[0], carry)
    for i in range(1, n):
        majority(a[i], b[i], a[i - 1])

    if carry_out is not None:
        operations.append(qml.CNOT(wires=[a[-1], carry_out]))

    for i in range(n - 1, 0, -1):
        unmajority_add(a[i], b[i], a[i - 1])
    unmajority_add(a[0], b[0], carry)

    return qml.tape.QuantumScript(operations)
