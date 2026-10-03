# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda

def create_state_prep():
    qvm = pyqpanda.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = pyqpanda.QProg()
    prog << pyqpanda.X(q[0])
    return prog
