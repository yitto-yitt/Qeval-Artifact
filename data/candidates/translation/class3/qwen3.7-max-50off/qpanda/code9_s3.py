# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, Var, RY, RZ, CNOT, Barrier

def create_efficientSU2():
    q = [Qubit() for _ in range(3)]
    circ = QCircuit()
    
    params = []
    
    for i in range(3):
        p1 = Var(f"p{len(params)}")
        p2 = Var(f"p{len(params)+1}")
        params.extend([p1, p2])
        circ << RY(q[i], p1)
        circ << RZ(q[i], p2)
        
    circ << Barrier(q)
    
    circ << CNOT(q[2], q[1])
    circ << CNOT(q[1], q[0])
    
    circ << Barrier(q)
    
    for i in range(3):
        p1 = Var(f"p{len(params)}")
        p2 = Var(f"p{len(params)+1}")
        params.extend([p1, p2])
        circ << RY(q[i], p1)
        circ << RZ(q[i], p2)
        
    circ << Barrier(q)
    
    return circ
