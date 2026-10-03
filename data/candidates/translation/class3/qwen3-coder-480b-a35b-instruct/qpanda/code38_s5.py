# EVAL_META: task_id=38, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CRZ(theta, q[0], q[1]))
    prog.insert(pq.H(q[1]))
    prog.insert(pq.CRY(theta, q[1], q[0]))
    
    return prog
