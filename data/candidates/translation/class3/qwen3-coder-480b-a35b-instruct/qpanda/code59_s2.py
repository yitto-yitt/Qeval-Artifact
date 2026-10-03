# EVAL_META: task_id=59, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_cz_gate():
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[1]) << pq.CNOT(qubits[0], qubits[1]) << pq.H(qubits[1])
    
    return prog
