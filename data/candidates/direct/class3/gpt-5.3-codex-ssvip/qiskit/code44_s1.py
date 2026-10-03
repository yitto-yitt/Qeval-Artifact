# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit


def tensor_circuits():
    qc1 = QuantumCircuit(1)
    qc1.x(0)

    qc2 = QuantumCircuit(2)
    qc2.cry(0.2, 0, 1)

    return qc2.tensor(qc1)
