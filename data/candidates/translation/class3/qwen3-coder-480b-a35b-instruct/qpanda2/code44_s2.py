# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def tensor_circuits():
    qubits_top = machine.qAlloc_many(1)
    qubits_bottom = machine.qAlloc_many(2)
    
    prog_top = pq.QProg()
    prog_top.insert(pq.X(qubits_top[0]))
    
    prog_bottom = pq.QProg()
    prog_bottom.insert(pq.CRY(qubits_bottom[0], qubits_bottom[1], 0.2))
    
    tensored_prog = pq.tensor(prog_bottom, prog_top)
    
    return tensored_prog

machine.finalize()
