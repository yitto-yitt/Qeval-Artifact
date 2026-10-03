# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    ops = [
        qml.H(wires=1),
        qml.H(wires=2),
        qml.CNOT(wires=[1, 3]),
        qml.CNOT(wires=[2, 4]),
    ]
    tape = qml.tape.QuantumScript(ops)
    return qml.adjoint(tape)
