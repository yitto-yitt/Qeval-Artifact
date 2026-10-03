# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Parameter

def create_efficientSU2():
    qc = QCircuit()
    q = [0, 1, 2]
    params = [Parameter(f"p{i}") for i in range(12)]
    
    qc.ry(q[0], params[0])
    qc.ry(q[1], params[1])
    qc.ry(q[2], params[2])
    qc.rz(q[0], params[3])
    qc.rz(q[1], params[4])
    qc.rz(q[2], params[5])
    
    qc.barrier(q)
    
    qc.cx(q[2], q[1])
    qc.cx(q[1], q[0])
    
    qc.barrier(q)
    
    qc.ry(q[0], params[6])
    qc.ry(q[1], params[7])
    qc.ry(q[2], params[8])
    qc.rz(q[0], params[9])
    qc.rz(q[1], params[10])
    qc.rz(q[2], params[11])
    
    return qc
