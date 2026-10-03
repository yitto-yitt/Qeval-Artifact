# EVAL_META: task_id=60, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_cy_gate():
    qc = QuantumCircuit(2, name="cy_one_cx")
    qc.sdg(1)
    qc.cx(0, 1)
    qc.s(1)
    return qc
