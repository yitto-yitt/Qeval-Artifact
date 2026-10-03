# EVAL_META: task_id=58, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_ch_gate():
    qc = QuantumCircuit(2)
    qc.ry(-3.14159/4, 1)
    qc.cx(0, 1)
    qc.ry(3.14159/4, 1)
    qc.cx(0, 1)
    qc.ry(-3.14159/4, 1)
    return qc
