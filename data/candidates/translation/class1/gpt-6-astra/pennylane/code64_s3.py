# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    secret = s[::-1]
    reg1 = [("reg1", i) for i in range(n)]
    reg2 = [("reg2", i) for i in range(n)]
    device = qml.device("default.qubit", wires=reg1 + reg2)

    @qml.set_shots(shots=1)
    @qml.qnode(device)
    def circuit():
        for wire in reg1:
            qml.Hadamard(wires=wire)

        qml.Barrier(wires=reg1 + reg2)

        for source, target in zip(reg1, reg2):
            qml.CNOT(wires=[source, target])

        if "1" in secret:
            pivot = secret.find("1")
            for j, bit in enumerate(secret):
                if bit == "1":
                    qml.CNOT(wires=[reg1[pivot], reg2[j]])

            qml.Barrier(wires=reg1 + reg2)

            for wire in reg1:
                qml.Hadamard(wires=wire)

        return qml.sample(wires=reg1[::-1])

    circuit.classical_registers = {"c": tuple(reg1)}
    return circuit
