# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda import *

def qft_no_swaps(num_qubits):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    cbits = qvm.cAlloc_many(num_qubits)
    
    prog = QProg()
    prog.insert(qft_dagger(qubits, num_qubits))
    
    return prog
