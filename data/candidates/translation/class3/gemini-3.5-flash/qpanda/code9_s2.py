# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_efficientSU2():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    
    prog = pq.QProg()
    
    # Layer 0: Rotations
    for i in range(3):
        prog << pq.RY(qubits[i], 0.0)
        prog << pq.RZ(qubits[i], 0.0)
        
    # Barrier
    prog << pq.BARRIER(qubits)
    
    # Layer 1: Entanglement (Circular)
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[1], qubits[2])
    prog << pq.CNOT(qubits[2], qubits[0])
    
    # Barrier
    prog << pq.BARRIER(qubits)
    
    # Layer 2: Rotations
    for i in range(3):
        prog << pq.RY(qubits[i], 0.0)
        prog << pq.RZ(qubits[i], 0.0)
        
    return prog
