# EVAL_META: task_id=23, framework=qpanda, class=3
import pyqpanda3.core as pq

def dj_constant_oracle():
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.X(q[2]))
    
    qvm.finalize()
    return prog
