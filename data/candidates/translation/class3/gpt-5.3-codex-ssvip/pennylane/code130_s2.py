# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    ops = []
    for i in range(2):
        ops.append(qml.Hadamard(wires=i + 1))
    for i in range(2):
        ops.append(qml.CNOT(wires=[i + 1, i + 3]))
    return qml.tape.QuantumScript(ops).adjoint()
