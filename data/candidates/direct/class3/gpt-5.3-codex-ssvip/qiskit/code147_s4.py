# EVAL_META: task_id=147, framework=qiskit, class=3
from qiskit import QuantumCircuit

def mcy(qc):
    qc.mcy([0, 1, 2, 3], 4)
    return qc
