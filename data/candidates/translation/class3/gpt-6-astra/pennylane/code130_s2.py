# EVAL_META: task_id=130, framework=pennylane, class=3
import operator
import pennylane as qml


def inv_circuit(n):
    n = operator.index(n)
    if n < 5:
        raise ValueError("The circuit requires at least five qubits.")

    operations = [
        qml.Identity(wires=wire)
        for wire in range(n)
        if wire not in (1, 2, 3, 4)
    ]
    operations.extend([
        qml.CNOT(wires=[2, 4]),
        qml.CNOT(wires=[1, 3]),
        qml.Hadamard(wires=2),
        qml.Hadamard(wires=1),
    ])
    return qml.tape.QuantumScript(operations)
