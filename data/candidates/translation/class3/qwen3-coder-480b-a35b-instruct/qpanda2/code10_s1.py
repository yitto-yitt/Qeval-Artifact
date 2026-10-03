# EVAL_META: task_id=10, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_operator():
    # Define the unitary matrix
    unitary_matrix = np.array([[0, 0, 0, 1], 
                               [0, 0, 1, 0], 
                               [0, 1, 0, 0], 
                               [1, 0, 0, 0]], dtype=complex)
    
    # Create a quantum program
    prog = pq.QProg()
    
    # Add the unitary operation using U4 gate (general 2-qubit gate)
    prog.insert(pq.unitary_decompose(unitary_matrix, qubits))
    
    # Since pyQPanda doesn't have direct transpilation like Qiskit,
    # we just return the program with the decomposed gates
    return prog

# Clean up
machine.finalize()
