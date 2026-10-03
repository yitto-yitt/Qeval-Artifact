# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml
from pennylane.circuit_graph import CircuitGraph


def bell_dag():
    ops = [qml.Hadamard(wires=0), qml.CNOT(wires=[0, 1])]
    measurements = [qml.probs(wires=0)]
    return CircuitGraph(ops, measurements, wires=[0, 1, 2])
