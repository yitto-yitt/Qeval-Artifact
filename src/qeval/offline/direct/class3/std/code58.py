# EVAL_META: task_id=58, framework=qiskit, class=3

from qiskit import QuantumCircuit
from numpy import pi

def create_ch_gate():
    circuit = QuantumCircuit(2)
    circuit.ry(pi/4, 1)
    circuit.cx(0,1)
    circuit.ry(-pi/4, 1)
    return circuit


# ==================================================
