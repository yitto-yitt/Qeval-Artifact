# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape


def apply_op_back():
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
    ]
    tape = QuantumTape(ops, [])
    tape.append(qml.Hadamard(wires=0))
    return tape
