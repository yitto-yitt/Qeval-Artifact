# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda import *
import numpy as np

def create_diagonal_circuit(diag):
    # Convert diag to numpy array
    diag_array = np.array(diag, dtype=complex)
    
    # Calculate number of qubits needed
    num_qubits = int(np.log2(len(diag_array)))
    
    # Create machine and allocate qubits
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(num_qubits)
    cbits = machine.cAlloc_many(num_qubits)
    
    # Create the quantum program
    prog = QProg()
    
    # Create diagonal matrix from diagonal elements
    # In pyQPanda, we need to create a custom gate for diagonal operations
    # We'll use the unitary matrix approach where the diagonal elements form the diagonal of a unitary matrix
    diagonal_matrix = np.diag(diag_array)
    
    # Create a custom gate from the diagonal matrix
    custom_gate = create_unitary_gate(diagonal_matrix, qubits)
    
    # Add the custom gate to the program
    prog.insert(custom_gate)
    
    # Measure all qubits
    for i in range(num_qubits):
        prog.insert(measure(qubits[i], cbits[i]))
    
    return prog
