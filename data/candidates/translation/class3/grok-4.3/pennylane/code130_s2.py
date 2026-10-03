# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    tape = qml.tape.QuantumTape()
    with tape:
        for i in range(2):
            qml.Hadamard(wires=i+1)
        for i in range(2):
            qml.CNOT(wires=[i+1, i+3])
    return tape.adjoint()
