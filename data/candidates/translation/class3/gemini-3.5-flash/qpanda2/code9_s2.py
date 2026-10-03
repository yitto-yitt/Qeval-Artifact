# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    prog = pq.QProg()
    
    # Layer 0: RY and RZ on all qubits
    for i in range(3):
        prog << pq.RY(q[i], 0.0)
        prog << pq.RZ(q[i], 0.0)
        
    # Barrier 1
    prog << pq.BARRIER(q)
    
    # Entanglement layer: CNOT(2, 1), CNOT(1, 0)
    prog << pq.CNOT(q[2], q[1])
    prog << pq.CNOT(q[1], q[0])
    
    # Barrier 2
    prog << pq.BARRIER(q)
    
    # Layer 1: RY and RZ on all qubits
    for i in range(3):
        prog << pq.RY(q[i], 0.0)
        prog << pq.RZ(q[i], 0.0)
        
    return prog

machine.finalize()
