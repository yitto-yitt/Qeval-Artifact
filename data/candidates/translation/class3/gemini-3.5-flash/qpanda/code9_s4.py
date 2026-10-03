# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_efficientSU2():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    prog = pq.QProg()
    
    # Rep 0: Rotation layer
    prog.insert(pq.RY(q[0], 0.0))
    prog.insert(pq.RZ(q[0], 0.0))
    prog.insert(pq.RY(q[1], 0.0))
    prog.insert(pq.RZ(q[1], 0.0))
    prog.insert(pq.RY(q[2], 0.0))
    prog.insert(pq.RZ(q[2], 0.0))
    
    # Barrier
    prog.insert(pq.BARRIER(q))
    
    # Entanglement layer (reverse_linear)
    prog.insert(pq.CNOT(q[2], q[1]))
    prog.insert(pq.CNOT(q[1], q[0]))
    
    # Barrier
    prog.insert(pq.BARRIER(q))
    
    # Final Rotation layer
    prog.insert(pq.RY(q[0], 0.0))
    prog.insert(pq.RZ(q[0], 0.0))
    prog.insert(pq.RY(q[1], 0.0))
    prog.insert(pq.RZ(q[1], 0.0))
    prog.insert(pq.RY(q[2], 0.0))
    prog.insert(pq.RZ(q[2], 0.0))
    
    return prog
