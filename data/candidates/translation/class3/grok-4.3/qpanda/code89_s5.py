# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H

def create_controlled_hgate():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    prog = QProg()
    ch_gate = H(qubits[2]).control([qubits[0], qubits[1]])
    prog.insert(ch_gate)
    return prog
