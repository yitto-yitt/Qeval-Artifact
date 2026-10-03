# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit

def tensor_circuits():
    qc_1q = QuantumCircuit(1)
    qc_1q.x(0)
    qc_2q = QuantumCircuit(2)
    qc_2q.cry(0.2, 0, 1)
    return qc_2q.tensor(qc_1q)
