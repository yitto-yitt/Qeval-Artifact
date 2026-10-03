# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import *
def create_quantum_circuit(n_qubits):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n_qubits)
    prog = QProg()
    return prog
