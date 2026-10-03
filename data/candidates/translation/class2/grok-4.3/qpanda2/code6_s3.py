# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import QProg, X, qAlloc_many


def create_state_prep(num_qubits):
    qc = QProg()
    qv = qAlloc_many(num_qubits)
    qc << X(qv[0])
    return qc
