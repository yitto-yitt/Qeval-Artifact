# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, allocate_qubits, CNOT, T, X

def compose_cnot_dihedral():
    q = allocate_qubits(2)
    
    circ1 = QCircuit()
    circ1 << CNOT(q[0], q[1])
    circ1 << T(q[0])
    
    circ2 = QCircuit()
    circ2 << CNOT(q[0], q[1])
    circ2 << T(q[0])
    circ2 << X(q[1])
    
    composed = QCircuit()
    composed << circ1
    composed << circ2
    
    return composed
