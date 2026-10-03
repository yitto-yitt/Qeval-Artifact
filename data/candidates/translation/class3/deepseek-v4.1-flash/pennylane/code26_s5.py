# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript


def bell_dag():
    ops = [qml.Hadamard(wires=0), qml.CNOT(wires=[0, 1]), qml.Identity(wires=2)]
    measurements = [qml.sample(wires=0)]
    return QuantumScript(ops, measurements)
