# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit, transpile

def create_operator():
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.x(1)
    qc.cx(0, 1)
    return transpile(qc, basis_gates=["u", "cx"], optimization_level=1)
