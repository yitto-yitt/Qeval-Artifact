# EVAL_META: task_id=49, framework=qpanda, class=3
import pyqpanda3.core as pq

def simple_elitzur_vaidman():
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.H(qubits[0]))
    
    return prog
