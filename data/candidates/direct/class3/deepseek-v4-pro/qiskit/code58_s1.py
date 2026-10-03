# EVAL_META: task_id=58, framework=qiskit, class=3
from qiskit import QuantumCircuit
from math import pi

def create_ch_gate():
    qc = QuantumCircuit(2)
    qc.ry(pi/4, 1)
    qc.cx(0, 1)
    qc.ry(-pi/4, 1)
    return qc
