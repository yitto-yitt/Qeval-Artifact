# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq

_global_machine = None

def create_state_prep():
    global _global_machine
    _global_machine = pq.CPUQVM()
    _global_machine.init_qvm()
    q = _global_machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.X(q[0])
    return prog
