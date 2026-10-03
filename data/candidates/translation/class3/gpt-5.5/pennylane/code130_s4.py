# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    if n < 5:
        raise ValueError("n must be at least 5")

    ops = [
        qml.CNOT(wires=[2, 4]),
        qml.CNOT(wires=[1, 3]),
        qml.Hadamard(wires=2),
        qml.Hadamard(wires=1),
    ]

    return qml.tape.QuantumScript(ops, [])
