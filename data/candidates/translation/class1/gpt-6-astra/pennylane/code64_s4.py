# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    secret = s[::-1]
    device = qml.device("default.qubit", wires=2 * n)

    @qml.set_shots(shots=1)
    @qml.qnode(device)
    def circuit():
        for i in range(n):
            qml.Hadamard(wires=i)

        qml.Barrier(wires=range(2 * n), only_visual=True)

        for i in range(n):
            qml.CNOT(wires=[i, n + i])

        if "1" in secret:
            control = secret.find("1")
            for j, bit in enumerate(secret):
                if bit == "1":
                    qml.CNOT(wires=[control, n + j])

            qml.Barrier(wires=range(2 * n), only_visual=True)

            for i in range(n):
                qml.Hadamard(wires=i)

        return qml.sample(wires=list(reversed(range(n))))

    return circuit
