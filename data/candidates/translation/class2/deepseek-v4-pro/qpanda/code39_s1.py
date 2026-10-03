# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import QProg, QVM, H
import numpy as np

def create_uniform_superposition(n):
    qvm = QVM()
    qubits = qvm.qAlloc_many(n)
    prog = QProg()
    for i in range(n):
        prog << H(qubits[i])
    qvm.run(prog)
    statevector = qvm.getStatevector(qubits)
    return statevector
