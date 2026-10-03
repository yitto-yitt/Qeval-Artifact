# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml

def apply_op_back():
    tape = qml.tape.QuantumTape()
    tape.append(qml.Hadamard(wires=0))
    tape.append(qml.CNOT(wires=[0, 1]))
    tape.append(qml.Hadamard(wires=0))
    return tape
