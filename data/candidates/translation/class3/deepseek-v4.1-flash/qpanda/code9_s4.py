# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    num_qubits = 3
    reps = 1
    insert_barriers = True
    
    q = QVec(num_qubits)
    circuit = QCircuit()
    
    params = [var(0.0) for _ in range(12)]
    
    # Rotation layer 0
    for i in range(num_qubits):
        circuit << RY(q[i], params[i*2])
        circuit << RZ(q[i], params[i*2+1])
    if insert_barriers:
        circuit << BARRIER(q)
    
    # Entanglement layer
    for control, target in [[0,1], [0,2], [1,2]]:
        circuit << CNOT(q[control], q[target])
    if insert_barriers:
        circuit << BARRIER(q)
    
    # Rotation layer 1
    for i in range(num_qubits):
        circuit << RY(q[i], params[6 + i*2])
        circuit << RZ(q[i], params[6 + i*2+1])
    if insert_barriers:
        circuit << BARRIER(q)
    
    return circuit
