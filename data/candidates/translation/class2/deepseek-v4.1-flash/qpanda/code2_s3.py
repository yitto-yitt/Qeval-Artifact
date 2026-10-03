# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H, CNOT

def create_bell_statevector():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    qvm.run(prog)
    result = qvm.result()
    state = result.get_state_vector()
    return state
