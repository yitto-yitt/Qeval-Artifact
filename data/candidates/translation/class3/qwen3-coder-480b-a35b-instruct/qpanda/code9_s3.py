# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_efficientSU2():
    # Create a quantum program
    prog = pq.QProg()
    
    # Create 3 qubits
    qubits = pq.qAlloc_many(3)
    
    # Create 1 rep of SU2-like structure manually since pyqpanda doesn't have EfficientSU2
    # EfficientSU2 typically consists of alternating rotation layers and entanglement layers
    # Each layer has single-qubit rotations followed by entangling gates
    
    # First layer: single-qubit rotations on all qubits
    for i in range(3):
        prog << pq.RY(qubits[i], pq.Parameter(f"theta_{i}_0"))
        prog << pq.RZ(qubits[i], pq.Parameter(f"theta_{i}_1"))
    
    # Add barrier
    prog << pq.Barrier(qubits)
    
    # Entangling layer: CNOTs between adjacent qubits
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[1], qubits[2])
    
    # Second layer: single-qubit rotations
    for i in range(3):
        prog << pq.RY(qubits[i], pq.Parameter(f"theta_{i}_2"))
        prog << pq.RZ(qubits[i], pq.Parameter(f"theta_{i}_3"))
    
    # Add final barrier
    prog << pq.Barrier(qubits)
    
    return prog
