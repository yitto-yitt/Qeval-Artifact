# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    top_prog = pq.QProg()
    top_prog.insert(pq.X(qubits[0]))
    
    bottom_prog = pq.QProg()
    bottom_prog.insert(pq.CRY(qubits[0], qubits[1], 0.2))
    
    tensored_prog = bottom_prog * top_prog
    return tensored_prog

machine.finalize()
