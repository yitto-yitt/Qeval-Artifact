# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    # In pyQPanda, we need to decompose multi-controlled gates manually
    # C3SX can be implemented as a multi-controlled X gate with 3 controls
    # Using Toffoli gates and single-qubit rotations
    
    # First, we'll implement a multi-controlled X gate with 3 controls
    # This requires ancilla qubits for decomposition, but for simplicity
    # we'll use pyQPanda's built-in functionality where possible
    
    # For C3SX (controlled by qubits 0,1,2 and acting on qubit 3)
    # We'll use CNOT and CCNOT (Toffoli) gates
    
    # The SX gate is equivalent to sqrt(X), which is RY(pi/2)
    # So C3SX is a controlled version of this operation
    
    # Implementation using multi-controlled rotation
    prog << pq.CU(3.14159/2, 3.14159/2, -3.14159/2, 3.14159/2)[qubits[0], qubits[1], qubits[2], qubits[3]]
    
    return prog

# Clean up
machine.finalize()
