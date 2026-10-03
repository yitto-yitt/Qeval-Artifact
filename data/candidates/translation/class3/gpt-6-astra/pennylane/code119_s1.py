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
        carry_in = 0
        carry_out = 2 * n + 1
    elif kind == "half":
        carry_in = 2 * n + 1
        carry_out = 2 * n
    else:
        carry_in = 2 * n
        carry_out = None

    with qml.tape.QuantumTape() as circuit:
        for i in range(n):
            carry = carry_in if i == 0 else a[i - 1]
            qml.CNOT(wires=[a[i], b[i]])
            qml.CNOT(wires=[a[i], carry])
            qml.Toffoli(wires=[carry, b[i], a[i]])

        if carry_out is not None:
            qml.CNOT(wires=[a[-1], carry_out])

        for i in reversed(range(n)):
            carry = carry_in if i == 0 else a[i - 1]
            qml.Toffoli(wires=[carry, b[i], a[i]])
            qml.CNOT(wires=[a[i], carry])
            qml.CNOT(wires=[carry, b[i]])

    return circuit
