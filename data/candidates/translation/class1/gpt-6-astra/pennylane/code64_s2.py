# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    secret = s[::-1]
    device = qml.device("default.qubit", wires=2 * n)

    @qml.qnode(device)
    def circuit():
        for wire in range(n):
            qml.Hadamard(wires=wire)

        qml.Barrier(wires=range(2 * n), only_visual=True)

        for wire in range(n):
            qml.CNOT(wires=[wire, n + wire])

        if "1" in secret:
            pivot = secret.find("1")
            for wire, bit in enumerate(secret):
                if bit == "1":
                    qml.CNOT(wires=[pivot, n + wire])

            qml.Barrier(wires=range(2 * n), only_visual=True)

            for wire in range(n):
                qml.Hadamard(wires=wire)

        return qml.probs(wires=list(reversed(range(n))))

    circuit.classical_registers = {"c": tuple(range(n))}
    circuit()
    return circuit
