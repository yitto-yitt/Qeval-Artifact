# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_efficientSU2():
    # Create a quantum program with 3 qubits
    prog = pq.QProg()
    q = pq.qAlloc(3)
    
    # In pyQPanda3, we need to manually construct the EfficientSU2-like circuit
    # This involves alternating layers of single-qubit rotations and entangling gates
    # with barriers between layers
    
    # First layer: single-qubit rotations on all qubits
    for i in range(3):
        prog << pq.RY(q[i], pq.Parameter(f'theta_{i*2}'))
        prog << pq.RZ(q[i], pq.Parameter(f'theta_{i*2+1}'))
    
    # Add barrier
    prog << pq.Barrier(q)
    
    # Entangling layer: CNOTs between adjacent qubits
    prog << pq.CNOT(q[0], q[1])
    prog << pq.CNOT(q[1], q[2])
    
    # Second layer: single-qubit rotations on all qubits
    for i in range(3):
        prog << pq.RY(q[i], pq.Parameter(f'theta_{6+i*2}'))
        prog << pq.RZ(q[i], pq.Parameter(f'theta_{6+i*2+1}'))
    
    # Add final barrier
    prog << pq.Barrier(q)
    
    return prog
