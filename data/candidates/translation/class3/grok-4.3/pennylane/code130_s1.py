# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    ops = [qml.Hadamard(i + 1) for i in range(2)]
    ops += [qml.CNOT(wires=[i + 1, i + 3]) for i in range(2)]
    tape = qml.tape.QuantumScript(ops)
    return tape.adjoint()
