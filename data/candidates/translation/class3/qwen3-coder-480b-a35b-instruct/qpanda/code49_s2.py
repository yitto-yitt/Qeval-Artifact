# EVAL_META: task_id=49, framework=qpanda, class=3
import pyqpanda3.core as pq

def simple_elitzur_vaidman():
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.H(q[0]))
    
    qvm.finalize()
    return prog
