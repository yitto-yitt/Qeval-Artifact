# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qalloc_many(3)
    
    vqc = VariationalQuantumCircuit()
    
    # 12 parameters for 2 rotation layers (each has 3 RY and 3 RZ)
    params = [var(0.0, True) for _ in range(12)]
    
    # Rep 0 - Rotation Layer
    for i in range(3):
        vqc.insert(RY(q[i], params[i]))
    for i in range(3):
        vqc.insert(RZ(q[i], params[3 + i]))
        
    # Barrier
    vqc.insert(BARRIER(q))
    
    # Rep 0 - Entanglement Layer (circular)
    vqc.insert(CNOT(q[0], q[1]))
    vqc.insert(CNOT(q[1], q[2]))
    vqc.insert(CNOT(q[2], q[0]))
    
    # Barrier
    vqc.insert(BARRIER(q))
    
    # Final Rotation Layer
    for i in range(3):
        vqc.insert(RY(q[i], params[6 + i]))
    for i in range(3):
        vqc.insert(RZ(q[i], params[9 + i]))
        
    return vqc
