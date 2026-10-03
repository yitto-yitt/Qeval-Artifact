# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq

def create_ghz(drawing=False):
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.CNOT(q[0], q[2])
    prog << pq.measure_all(q, c)
    
    if drawing:
        return prog, pq.draw(prog)
    return prog
