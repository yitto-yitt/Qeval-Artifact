# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def tensor_circuits():
    qubits_1 = machine.qAlloc_many(1)
    qubits_2 = machine.qAlloc_many(2)
    
    top_prog = pq.QProg()
    top_prog.insert(pq.X(qubits_1[0]))
    
    bottom_prog = pq.QProg()
    bottom_prog.insert(pq.CRY(qubits_2[0], qubits_2[1], 0.2))
    
    tensored_prog = pq.tensor(bottom_prog, top_prog)
    
    return tensored_prog

machine.finalize()
