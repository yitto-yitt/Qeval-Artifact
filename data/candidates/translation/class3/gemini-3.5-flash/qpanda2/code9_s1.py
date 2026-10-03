# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    prog = pq.QProg()
    
    # SU2 layer 0
    for i in range(3):
        prog << pq.RY(q[i], 0.0)
        prog << pq.RZ(q[i], 0.0)
        
    # Barrier
    prog << pq.BARRIER(q)
    
    # Entanglement layer (reverse_linear)
    prog << pq.CNOT(q[2], q[1])
    prog << pq.CNOT(q[1], q[0])
    
    # Barrier
    prog << pq.BARRIER(q)
    
    # SU2 layer 1
    for i in range(3):
        prog << pq.RY(q[i], 0.0)
        prog << pq.RZ(q[i], 0.0)
        
    return prog

# Manual Cleanup
machine.finalize()
