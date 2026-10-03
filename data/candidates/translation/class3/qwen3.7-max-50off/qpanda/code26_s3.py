# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QuantumRegister, ClassicalRegister, QCircuit, QProg, H, CNOT, Measure

def bell_dag():
    q = QuantumRegister(3, "q")
    c = ClassicalRegister(3, "c")
    
    circ = QCircuit()
    circ << H(q[0])
    circ << CNOT(q[0], q[1])
    circ << Measure(q[0], c[0])
    
    prog = QProg()
    prog << circ
    
    return prog
