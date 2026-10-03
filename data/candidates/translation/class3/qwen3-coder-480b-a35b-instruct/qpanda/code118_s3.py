# EVAL_META: task_id=118, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_c3sx_circuit():
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(4)
    
    prog = pq.QProg()
    # In pyQPanda3, we need to decompose C3SX gate manually
    # C3SX is a 3-controlled sqrt(X) gate, which can be implemented using Toffoli gates and single-qubit rotations
    
    # Implementing C3SX using ancilla-free decomposition
    # First apply Hadamard on target qubit
    prog << pq.H(q[3])
    # Apply controlled-Rz(-pi/8) with controls [q0, q1, q2] and target q[3]
    # This requires multiple steps using Toffoli gates and single-qubit rotations
    # For simplicity, using the built-in multi-control X gate approach with proper decomposition
    
    # Using multi-controlled X gate implementation in pyQPanda3
    # C3SX = C3X with additional S† and H gates around it
    prog << pq.RZ(q[3], -pq.PI/4)  # Equivalent to part of SX decomposition
    
    # Implement multi-controlled X gate using decomposition
    # We'll use the standard decomposition for 3-controlled X gate
    ancilla = qvm.qAlloc()
    
    # C2X (Toffoli) between q[0], q[1] -> ancilla
    prog << pq.TOFFOLI(q[0], q[1], ancilla)
    # C2X between ancilla, q[2] -> q[3] 
    prog << pq.TOFFOLI(ancilla, q[2], q[3])
    # C2X (Toffoli) between q[0], q[1] -> ancilla
    prog << pq.TOFFOLI(q[0], q[1], ancilla)
    # Additional rotation for SX
    prog << pq.RZ(q[3], pq.PI/4)
    prog << pq.H(q[3])
    
    # Deallocate ancilla
    qvm.qFree(ancilla)
    
    return prog
