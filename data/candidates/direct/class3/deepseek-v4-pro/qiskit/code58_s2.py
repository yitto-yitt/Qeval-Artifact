# EVAL_META: task_id=58, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit

def create_ch_gate():
    qc = QuantumCircuit(2, name='CH')
    qc.ry(pi / 4, 1)
    qc.cx(0, 1)
    qc.ry(-pi / 4, 1)
    return qc
