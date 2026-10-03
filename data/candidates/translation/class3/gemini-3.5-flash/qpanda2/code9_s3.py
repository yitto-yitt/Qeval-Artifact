# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *

# Initialize CPUQVM globally
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = QCircuit()
    
    # Layer 0
    for i in range(3):
        circuit << RY(q[i], 0.0)
        circuit << RZ(q[i], 0.0)
        
    # Barrier
    circuit << Barrier(q)
    
    # Entanglement Layer (linear/local CX)
    circuit << CNOT(q[0], q[1])
    circuit << CNOT(q[1], q[2])
    
    # Barrier
    circuit << Barrier(q)
    
    # Layer 1
    for i in range(3):
        circuit << RY(q[i], 0.0)
        circuit << RZ(q[i], 0.0)
        
    return circuit

# Manual Cleanup
machine.finalize()
