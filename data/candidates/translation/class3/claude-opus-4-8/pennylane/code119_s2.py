# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    if kind == "full":
        num_qubits = 2 * n + 2
        cin = 0
        a = [1 + i for i in range(n)]
        b = [1 + n + i for i in range(n)]
        cout = 2 * n + 1
        c = cin
    elif kind == "half":
        num_qubits = 2 * n + 2
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cout = 2 * n
        c = 2 * n + 1
    elif kind == "fixed":
        num_qubits = 2 * n + 1
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        c = 2 * n
        cout = None
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'.")

    def maj(x, y, z):
        qml.CNOT(wires=[x, y])
        qml.CNOT(wires=[x, z])
        qml.Toffoli(wires=[z, y, x])

    def uma(x, y, z):
        qml.Toffoli(wires=[z, y, x])
        qml.CNOT(wires=[x, z])
        qml.CNOT(wires=[z, y])

    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        maj(c, b[0], a[0])
        for i in range(1, n):
            maj(a[i - 1], b[i], a[i])

        if kind in ["half", "full"]:
            qml.CNOT(wires=[a[n - 1], cout])

        for i in reversed(range(1, n)):
            uma(a[i - 1], b[i], a[i])
        uma(c, b[0], a[0])

        return qml.state()

    return circuit
