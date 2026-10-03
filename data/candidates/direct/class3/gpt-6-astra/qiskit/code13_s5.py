# EVAL_META: task_id=13, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def custom_rotation_gate():
    circuit = QuantumCircuit(1)
    circuit.u(pi / 2, pi / 2, pi / 2, 0)
    return circuit
