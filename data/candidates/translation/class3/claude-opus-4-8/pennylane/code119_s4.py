# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    if kind == "full":
        c = 0
        a = [1 + i for i in range(n)]
        b = [1 + n + i for i in range(n)]
        cout = 1 + 2 * n
        num_qubits = 2 * n + 2
        has_cout = True
    elif kind == "half":
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cout = 2 * n
        c = 2 * n + 1
        num_qubits = 2 * n + 2
        has_cout = True
    elif kind == "fixed":
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        c = 2 * n
        num_qubits = 2 * n + 1
        cout = None
        has_cout = False
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    def maj(wires):
        wa, wb, wc = wires
        qml.CNOT(wires=[wa, wb])
        qml.CNOT(wires=[wa, wc])
        qml.Toffoli(wires=[wc, wb, wa])

    def uma(wires):
        wa, wb, wc = wires
        qml.Toffoli(wires=[wc, wb, wa])
        qml.CNOT(wires=[wa, wc])
        qml.CNOT(wires=[wc, wb])

    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        maj([a[0], b[0], c])
        for i in range(1, n):
            maj([a[i], b[i], a[i - 1]])

        if has_cout:
            qml.CNOT(wires=[a[-1], cout])

        for i in reversed(range(1, n)):
            uma([a[i], b[i], a[i - 1]])
        uma([a[0], b[0], c])

        return qml.state()

    return circuit
