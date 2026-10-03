# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    ops = []
    for i in range(2):
        ops.append(qml.Hadamard(wires=i+1))
    for i in range(2):
        ops.append(qml.CNOT(wires=[i+1, i+2+1]))

    inverse_ops = [qml.adjoint(op) for op in reversed(ops)]
    return inverse_ops
