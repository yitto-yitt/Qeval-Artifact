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
                               [1, 0, 0, 0]])
    
    # Create a quantum program
    prog = pq.QProg()
    
    # Add the unitary operation using pyQPanda's built-in function
    prog.insert(pq.unitary_decompose(qubits, unitary_matrix))
    
    # Since pyQPanda doesn't have a direct equivalent to Qiskit's transpilation,
    # we just return the program with the decomposed unitary
    return prog

# Clean up
machine.finalize()
