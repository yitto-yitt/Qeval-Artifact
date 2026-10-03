# EVAL_META: task_id=60, framework=qpanda, class=3
import pyqpanda3 as pq

def create_cy_gate():
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.SDAG(qubits[1]) << pq.CNOT(qubits[0], qubits[1]) << pq.S(qubits[1])
    
    return prog
