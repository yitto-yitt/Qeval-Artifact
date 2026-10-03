# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit

def tensor_circuits():
    qc_x = QuantumCircuit(1)
    qc_x.x(0)

    qc_cry = QuantumCircuit(2)
    qc_cry.cry(0.2, 0, 1)

    return qc_x.tensor(qc_cry)
