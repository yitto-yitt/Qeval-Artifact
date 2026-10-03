# EVAL_META: task_id=109, framework=qpanda, class=3
import pyqpanda3.core as pq

def circuit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    
    vqc = pq.VariationalQuantumCircuit()
    vqc.insert(pq.H(q[0]))
    
    theta = pq.var(0.0, True)
    vqc.insert(pq.VariationalQuantumGate_RZ(q[0], theta))
    
    vqc.machine = machine
    return vqc
