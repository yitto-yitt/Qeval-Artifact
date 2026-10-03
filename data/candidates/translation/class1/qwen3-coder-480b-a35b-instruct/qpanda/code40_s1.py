# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda import *
import numpy as np

def init_random_3qubit(desired_vector):
    # Normalize the input vector
    desired_vector = np.array(desired_vector)
    desired_vector = desired_vector / np.linalg.norm(desired_vector)
    
    # Initialize QPanda environment
    qvm = CPUQVM()
    qvm.init_qvm()
    
    # Allocate 3 qubits and 3 classical bits
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    # Create the quantum program
    prog = QProg()
    
    # Initialize the quantum state to the desired vector
    prog.insert(initialize_qstate(qubits, desired_vector.tolist()))
    
    # Measure all qubits
    for i in range(3):
        prog.insert(measure(qubits[i], cbits[i]))
    
    # Run the program
    result = qvm.run_with_configuration(prog, cbits, 8192)
    
    # Convert results to probability distribution
    total = sum(result.values())
    prob_dist = {key: value / total for key, value in result.items()}
    
    # Clean up
    qvm.finalize()
    
    return prob_dist
