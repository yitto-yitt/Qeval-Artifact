# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y, QProg

def mcy(qc):
    q = qc.get_qvec()
    prog = QProg()
    prog << Y(q[4]).control([q[0], q[1], q[2], q[3]])
    qc << prog
    return qc
