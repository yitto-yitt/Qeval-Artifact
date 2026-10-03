# EVAL_META: task_id=59, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_cz_gate():
    qc = QuantumCircuit(2)
    qc.h(1)
    qc.cx(0, 1)
    qc.h(1)
    return qc
