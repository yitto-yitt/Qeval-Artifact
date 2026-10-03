# EVAL_META: task_id=49, framework=qiskit, class=3
from qiskit import QuantumCircuit

def simple_elitzur_vaidman():
    qc = QuantumCircuit(1)
    qc.h(0)
    return qc
