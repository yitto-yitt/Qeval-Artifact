# EVAL_META: task_id=36, framework=qpanda, class=3
import pyqpanda3.core as pq

def bv_function(s):
    n = len(s)
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n + 1)
    
    prog = pq.QProg()
    
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog.insert(pq.CNOT(qubits[index], qubits[n]))
    
    return prog
