# EVAL_META: task_id=66, framework=qiskit, class=2
from math import acos, pi, sqrt
from qiskit import QuantumCircuit


def w_state():
    circuit = QuantumCircuit(3)
    circuit.ry(2 * acos(1 / sqrt(3)), 0)
    circuit.cry(pi / 2, 0, 1)
    circuit.cx(1, 2)
    circuit.cx(0, 1)
    circuit.x(0)
    circuit.measure_all()
    return circuit
