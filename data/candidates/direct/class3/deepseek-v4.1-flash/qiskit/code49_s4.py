# EVAL_META: task_id=49, framework=qiskit, class=3
from qiskit import QuantumCircuit

def simple_elitzur_vaidman():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.x(2)
    qc.ccx(0, 2, 1)
    qc.h(0)
    return qc
