# EVAL_META: task_id=23, framework=qiskit, class=3
from qiskit import QuantumCircuit


def dj_constant_oracle():
    qc = QuantumCircuit(3)
    qc.x(2)
    return qc
