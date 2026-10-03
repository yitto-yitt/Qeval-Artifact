# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml
from pennylane.circuit_graph import CircuitGraph
from pennylane.wires import Wires


def bell_dag():
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.measure(0)

    return CircuitGraph(tape.operations, tape.measurements, Wires([0, 1, 2]))
