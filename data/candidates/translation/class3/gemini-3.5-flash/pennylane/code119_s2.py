# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == 'full':
        num_wires = 2 * n + 2
    elif kind == 'half':
        num_wires = 2 * n + 1
    elif kind == 'fixed':
        num_wires = 2 * n + 1
    else:
        raise ValueError("Invalid kind")

    dev = qml.device("default.qubit", wires=num_wires)

    def maj(c, b, a):
        qml.CNOT(wires=[a, b])
        qml.CNOT(wires=[a, c])
        qml.Toffoli(wires=[c, b, a])

    def uma(c, b, a):
        qml.Toffoli(wires=[c, b, a])
        qml.CNOT(wires=[a, c])
        qml.CNOT(wires=[c, b])

    @qml.qnode(dev)
    def circuit():
        if kind == 'full':
            for i in range(n):
                c = 0 if i == 0 else i
                b = n + 1 + i
                a = 1 + i
                maj(c, b, a)
            qml.CNOT(wires=[n, 2 * n + 1])
            for i in range(n - 1, -1, -1):
                c = 0 if i == 0 else i
                b = n + 1 + i
                a = 1 + i
                uma(c, b, a)
        elif kind == 'fixed':
            for i in range(n):
                c = 0 if i == 0 else i
                b = n + 1 + i
                a = 1 + i
                maj(c, b, a)
            for i in range(n - 1, -1, -1):
                c = 0 if i == 0 else i
                b = n + 1 + i
                a = 1 + i
                uma(c, b, a)
        elif kind == 'half':
            if n == 1:
                qml.Toffoli(wires=[0, 1, 2])
                qml.CNOT(wires=[0, 1])
            else:
                qml.CNOT(wires=[0, n])
                qml.Toffoli(wires=[0, n, 1])
                for i in range(1, n - 1):
                    qml.CNOT(wires=[i, n + i])
                    qml.CNOT(wires=[i, i - 1])
                    qml.Toffoli(wires=[i - 1, n + i, i])
                qml.CNOT(wires=[n - 1, 2 * n - 1])
                qml.CNOT(wires=[n - 1, n - 2])
                qml.Toffoli(wires=[n - 2, 2 * n - 1, n - 1])
                qml.CNOT(wires=[n - 1, 2 * n])
                qml.Toffoli(wires=[n - 2, 2 * n - 1, n - 1])
                qml.CNOT(wires=[n - 1, n - 2])
                qml.CNOT(wires=[n - 2, 2 * n - 1])
                for i in range(n - 2, 0, -1):
                    qml.Toffoli(wires=[i - 1, n + i, i])
                    qml.CNOT(wires=[i, i - 1])
                    qml.CNOT(wires=[i - 1, n + i])
                qml.Toffoli(wires=[0, n, 1])
                qml.CNOT(wires=[0, n])
        return qml.state()

    return circuit
