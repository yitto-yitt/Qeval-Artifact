# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, Var, QCircuit, RY, RZ, CNOT

def create_efficientSU2():
    qm = QuantumMachine()
    q = qm.qAlloc_many(3)
    params = [Var(f"theta_{i}") for i in range(12)]
    
    circ = QCircuit()
    
    # Rep 0 rotations
    circ << RY(q[0], params[0]) << RZ(q[0], params[1])
    circ << RY(q[1], params[2]) << RZ(q[1], params[3])
    circ << RY(q[2], params[4]) << RZ(q[2], params[5])
    
    # Entanglement layer
    circ << CNOT(q[0], q[1]) << CNOT(q[1], q[2])
    
    # Rep 1 rotations
    circ << RY(q[0], params[6]) << RZ(q[0], params[7])
    circ << RY(q[1], params[8]) << RZ(q[1], params[9])
    circ << RY(q[2], params[10]) << RZ(q[2], params[11])
    
    return circ
