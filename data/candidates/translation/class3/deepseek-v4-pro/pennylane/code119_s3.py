# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    if kind == "full":
        num_qubits = 2 * n + 2
    elif kind in ("half", "fixed"):
        num_qubits = 2 * n + 1
    else:
        raise ValueError(f"Unsupported kind: {kind}")

    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        carry = 2 * n

        for i in range(n):
            qml.CNOT(wires=[carry, n + i])
            qml.CNOT(wires=[carry, i])
            qml.Toffoli(wires=[i, n + i, carry])

        if kind == "full":
            qml.CNOT(wires=[carry, 2 * n + 1])

        for i in range(n - 1, -1, -1):
            qml.Toffoli(wires=[i, n + i, carry])
            qml.CNOT(wires=[carry, i])
            qml.CNOT(wires=[i, n + i])

        return qml.state()

    return circuit
