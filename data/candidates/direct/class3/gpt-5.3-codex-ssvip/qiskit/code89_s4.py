# EVAL_META: task_id=89, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_controlled_hgate():
    qc = QuantumCircuit(3)
    qc.ch(0, 2)
    qc.ch(1, 2)
    return qc
