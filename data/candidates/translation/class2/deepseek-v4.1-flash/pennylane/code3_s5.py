# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml
from pennylane.tape import QuantumScript
from pennylane.measurements import SampleMP

def create_ghz(drawing=False):
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[0, 2])
    ]
    measurements = [SampleMP(wires=[0, 1, 2])]
    tape = QuantumScript(ops, measurements)
    if drawing:
        return tape, qml.draw_mpl(tape)
    return tape
