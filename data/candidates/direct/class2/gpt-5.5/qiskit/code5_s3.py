# EVAL_META: task_id=5, framework=qiskit, class=2
from qiskit import QuantumCircuit


def create_state_prep():
    qc = QuantumCircuit(2)
    qc.x(0)
    return qc
