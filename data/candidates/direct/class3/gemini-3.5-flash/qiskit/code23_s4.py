# EVAL_META: task_id=23, framework=qiskit, class=3
from qiskit import QuantumCircuit

def dj_constant_oracle():
    oracle_qc = QuantumCircuit(3)
    oracle_qc.x(2)
    return oracle_qc
