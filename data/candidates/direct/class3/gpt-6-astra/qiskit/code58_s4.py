# EVAL_META: task_id=58, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def create_ch_gate():
    circuit = QuantumCircuit(2, name="CH")
    circuit.ry(pi / 4, 1)
    circuit.cx(0, 1)
    circuit.ry(-pi / 4, 1)
    return circuit
