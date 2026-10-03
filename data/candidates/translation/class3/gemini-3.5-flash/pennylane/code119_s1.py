# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind in ["full", "fixed"]:
        cin = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        cout = 2 * n + 1 if kind == "full" else None
    else:
        cin = None
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        cout = 2 * n

    def circuit():
        if n > 0:
            if kind in ["full", "fixed"]:
                qml.CNOT(wires=[a[0], b[0]])
                qml.CNOT(wires=[a[0], cin])
                qml.Toffoli(wires=[cin, b[0], a[0]])
                for i in range(1, n):
                    qml.CNOT(wires=[a[i], b[i]])
                    qml.CNOT(wires=[a[i], a[i - 1]])
                    qml.Toffoli(wires=[a[i - 1], b[i], a[i]])
            else:
                for i in range(1, n):
                    qml.CNOT(wires=[a[i], b[i]])
                    qml.CNOT(wires=[a[i], a[i - 1]])
                    qml.Toffoli(wires=[a[i - 1], b[i], a[i]])

            if kind in ["full", "half"]:
                qml.CNOT(wires=[a[n - 1], cout])

            if kind in ["full", "fixed"]:
                for i in reversed(range(1, n)):
                    qml.Toffoli(wires=[a[i - 1], b[i], a[i]])
                    qml.CNOT(wires=[a[i], a[i - 1]])
                    qml.CNOT(wires=[a[i - 1], b[i]])
                qml.Toffoli(wires=[cin, b[0], a[0]])
                qml.CNOT(wires=[a[0], cin])
                qml.CNOT(wires=[cin, b[0]])
            else:
                for i in reversed(range(1, n)):
                    qml.Toffoli(wires=[a[i - 1], b[i], a[i]])
                    qml.CNOT(wires=[a[i], a[i - 1]])
                    qml.CNOT(wires=[a[i - 1], b[i]])
                qml.CNOT(wires=[a[0], b[0]])

    return circuit
