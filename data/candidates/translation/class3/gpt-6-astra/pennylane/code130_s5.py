# EVAL_META: task_id=130, framework=pennylane, class=3
import operator
import pennylane as qml

def inv_circuit(n):
    n = operator.index(n)
    if n < 5:
        raise ValueError("The circuit requires at least five qubits.")

    with qml.tape.QuantumTape() as circuit:
        qml.Identity(wires=range(n))
        qml.CNOT(wires=[2, 4])
        qml.CNOT(wires=[1, 3])
        qml.Hadamard(wires=2)
        qml.Hadamard(wires=1)

    return circuit
