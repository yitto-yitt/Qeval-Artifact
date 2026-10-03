# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit, Qubit, CBit, Measure

def bell_dag():
    q = [Qubit() for _ in range(3)]
    c = [CBit() for _ in range(3)]
    
    circ = QCircuit()
    circ.h(q[0])
    circ.cx(q[0], q[1])
    
    prog = QProg()
    prog << circ
    prog << Measure(q[0], c[0])
    
    return prog
