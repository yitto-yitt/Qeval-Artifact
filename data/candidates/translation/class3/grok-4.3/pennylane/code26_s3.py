# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml
from pennylane.circuit_graph import CircuitGraph


def bell_dag():
    with qml.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.expval(qml.PauliZ(wires=0))
    dag = CircuitGraph(tape.operations, tape.measurements, tape.wires)
    return dag
