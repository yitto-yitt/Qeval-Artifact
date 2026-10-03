# EVAL_META: task_id=66, framework=qiskit, class=2
from math import acos, pi, sqrt
from qiskit import QuantumCircuit


def w_state():
    circuit = QuantumCircuit(3, 3)
    circuit.x(0)
    circuit.cry(2 * acos(1 / sqrt(3)), 0, 1)
    circuit.cx(1, 0)
    circuit.cry(pi / 2, 1, 2)
    circuit.cx(2, 1)
    circuit.measure(range(3), range(3))
    return circuit
