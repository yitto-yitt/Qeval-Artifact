# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    prog = pq.QProg()
    
    # Layer 0: SU2
    prog << pq.RY(q[0], 0.0) << pq.RY(q[1], 0.0) << pq.RY(q[2], 0.0)
    prog << pq.RZ(q[0], 0.0) << pq.RZ(q[1], 0.0) << pq.RZ(q[2], 0.0)
    
    # Barrier
    prog << pq.BARRIER(q)
    
    # Entanglement Layer (reverse_linear)
    prog << pq.CNOT(q[2], q[1]) << pq.CNOT(q[1], q[0])
    
    # Barrier
    prog << pq.BARRIER(q)
    
    # Layer 1: SU2
    prog << pq.RY(q[0], 0.0) << pq.RY(q[1], 0.0) << pq.RY(q[2], 0.0)
    prog << pq.RZ(q[0], 0.0) << pq.RZ(q[1], 0.0) << pq.RZ(q[2], 0.0)
    
    return prog

machine.finalize()
