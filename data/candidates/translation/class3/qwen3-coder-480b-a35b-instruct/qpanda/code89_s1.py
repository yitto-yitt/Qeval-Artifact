# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda.core import *

def create_controlled_hgate():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    prog = QProg()
    h_gate = H(qubits[2])
    c2h_gate = h_gate.control(qubits[0:2])
    prog.insert(c2h_gate)
    return prog
