# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq

def create_bell_statevector():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    
    if hasattr(pq, 'get_statevector'):
        sv = pq.get_statevector(prog, q)
    else:
        sv = pq.get_state_vector(prog, q)
        
    qvm.finalize()
    return sv
