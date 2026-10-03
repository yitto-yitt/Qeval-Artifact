# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    if kind == "full":
        cin = 0
        a = [1 + i for i in range(n)]
        b = [1 + n + i for i in range(n)]
        cout = 2 * n + 1
    elif kind == "half":
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cout = 2 * n
        cin = 2 * n + 1
    else:  # fixed
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cin = 2 * n
        cout = None

    def maj(x, y, z):
        qml.CNOT(wires=[x, y])
        qml.CNOT(wires=[x, z])
        qml.Toffoli(wires=[z, y, x])

    def uma(x, y, z):
        qml.Toffoli(wires=[z, y, x])
        qml.CNOT(wires=[x, z])
        qml.CNOT(wires=[z, y])

    with qml.tape.QuantumTape() as tape:
        # carry chain
        maj(a[0], b[0], cin)
        for i in range(1, n):
            maj(a[i], b[i], a[i - 1])

        if kind in ("full", "half"):
            qml.CNOT(wires=[a[n - 1], cout])

        # uncompute chain
        for i in reversed(range(1, n)):
            uma(a[i], b[i], a[i - 1])
        uma(a[0], b[0], cin)

    return tape
