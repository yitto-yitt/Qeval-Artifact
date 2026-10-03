# EVAL_META: task_id=23, framework=qpanda, class=3
import pyqpanda3.core as pq

def dj_constant_oracle():
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    prog = pq.QProg()
    prog.insert(pq.X(qubits[2]))
    return prog, qubits
