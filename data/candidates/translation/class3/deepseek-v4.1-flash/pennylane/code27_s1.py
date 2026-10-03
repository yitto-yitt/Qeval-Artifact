# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape
from pennylane.wires import Wires

def apply_op_back():
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.Hadamard(wires=0)
    ]
    tape = QuantumTape(ops=ops, measurements=[])
    tape._wires = Wires([0, 1, 2])
    return tape
