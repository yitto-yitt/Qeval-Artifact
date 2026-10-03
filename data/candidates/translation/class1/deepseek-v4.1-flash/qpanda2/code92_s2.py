# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import *

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    result = qvm.prob_run_dict(prog, qubits, -1)
    qvm.finalize()
    return result
