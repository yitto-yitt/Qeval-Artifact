# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    with qml.tape.QuantumTape() as tape:
        for i in reversed(range(2)):
            qml.CNOT(wires=[i+1, i+3])
        for i in reversed(range(2)):
            qml.Hadamard(wires=i+1)
    return tape
