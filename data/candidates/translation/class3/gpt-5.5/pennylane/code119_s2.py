# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1")

    ops = []
    n = num_state_qubits

    def maj(x, y, z):
        ops.append(qml.CNOT(wires=[z, y]))
        ops.append(qml.CNOT(wires=[z, x]))
        ops.append(qml.Toffoli(wires=[x, y, z]))

    def uma(x, y, z):
        ops.append(qml.Toffoli(wires=[x, y, z]))
        ops.append(qml.CNOT(wires=[z, x]))
        ops.append(qml.CNOT(wires=[x, y]))

    if kind == "full":
        cin = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        cout = 2 * n + 1
        num_qubits = 2 * n + 2

        maj(cin, b[0], a[0])
        for i in range(n - 1):
            maj(a[i], b[i + 1], a[i + 1])
        ops.append(qml.CNOT(wires=[a[-1], cout]))
        for i in reversed(range(n - 1)):
            uma(a[i], b[i + 1], a[i + 1])
        uma(cin, b[0], a[0])

    elif kind == "half":
        a = list(range(n))
        b = list(range(n, 2 * n))
        cout = 2 * n
        helper = 2 * n + 1
        num_qubits = 2 * n + 2

        maj(helper, b[0], a[0])
        for i in range(n - 1):
            maj(a[i], b[i + 1], a[i + 1])
        ops.append(qml.CNOT(wires=[a[-1], cout]))
        for i in reversed(range(n - 1)):
            uma(a[i], b[i + 1], a[i + 1])
        uma(helper, b[0], a[0])

    else:
        a = list(range(n))
        b = list(range(n, 2 * n))
        helper = 2 * n
        num_qubits = 2 * n + 1

        maj(helper, b[0], a[0])
        for i in range(n - 1):
            maj(a[i], b[i + 1], a[i + 1])
        for i in reversed(range(n - 1)):
            uma(a[i], b[i + 1], a[i + 1])
        uma(helper, b[0], a[0])

    return qml.tape.QuantumScript(ops, [], shots=None)
