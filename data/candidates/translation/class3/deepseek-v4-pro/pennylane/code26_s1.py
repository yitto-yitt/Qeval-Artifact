# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript
from pennylane.circuit_graph import CircuitGraph


def bell_dag():
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.measure(wires=0)
    ]
    tape = QuantumScript(ops, wire_order=[0, 1, 2])
    dag = CircuitGraph(tape)
    return dag
