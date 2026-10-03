# EVAL_META: task_id=57, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_swap_gate():
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.CX(qubits[0], qubits[1]))
    prog.insert(pq.CX(qubits[1], qubits[0]))
    prog.insert(pq.CX(qubits[0], qubits[1]))
    
    return prog
