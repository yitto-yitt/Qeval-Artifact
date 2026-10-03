# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CNOT, qAlloc_many

def simple_elitzur_vaidman():
    qubits = qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << H(qubits[0])
    return prog
