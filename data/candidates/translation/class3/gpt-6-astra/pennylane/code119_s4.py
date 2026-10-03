# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1.")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'.")

    n = num_state_qubits
    offset = 1 if kind == "full" else 0
    a = list(range(offset, offset + n))
    b = list(range(offset + n, offset + 2 * n))

    if kind == "full":
        carry = 0
        carry_out = 2 * n + 1
    elif kind == "half":
        carry = 2 * n + 1
        carry_out = 2 * n
    else:
        carry = 2 * n
        carry_out = None

    def majority(x, y, z):
        qml.CNOT(wires=[x, y])
        qml.CNOT(wires=[x, z])
        qml.Toffoli(wires=[z, y, x])

    def unmajority_add(x, y, z):
        qml.Toffoli(wires=[z, y, x])
        qml.CNOT(wires=[x, z])
        qml.CNOT(wires=[z, y])

    with qml.tape.QuantumTape() as circuit:
        majority(a[0], b[0], carry)

        for i in range(n - 1):
            majority(a[i + 1], b[i + 1], a[i])

        if carry_out is not None:
            qml.CNOT(wires=[a[-1], carry_out])

        for i in reversed(range(n - 1)):
            unmajority_add(a[i + 1], b[i + 1], a[i])

        unmajority_add(a[0], b[0], carry)

    return circuit
