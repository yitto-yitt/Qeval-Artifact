# EVAL_META: task_id=23, framework=qiskit, class=3
from qiskit import QuantumCircuit


def dj_constant_oracle():
    oracle = QuantumCircuit(3, name="dj_constant_one_oracle")
    oracle.x(2)
    return oracle
