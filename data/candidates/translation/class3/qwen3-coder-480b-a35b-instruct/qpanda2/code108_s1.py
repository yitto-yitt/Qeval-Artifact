# EVAL_META: task_id=108, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
qubits = machine.qAlloc_many(4)

def initialize_adjoint_and_compose(data1, data2):
    # Convert numpy arrays to the format expected by pyqpanda if needed
    choi1_matrix = np.array(data1)
    choi2_matrix = np.array(data2)
    
    # In pyqpanda, we need to work with quantum programs directly
    # Since pyqpanda doesn't have a direct Choi matrix class,
    # we simulate the behavior using density matrices or unitary operations
    
    # For this specific case, we'll return the matrices themselves
    # as pyqpanda does not have built-in Choi matrix operations
    choi1 = choi1_matrix
    choi2 = choi2_matrix
    adjoint_choi1 = np.conjugate(np.transpose(choi1))
    composed_choi = np.dot(choi1, choi2)
    
    return choi1, adjoint_choi1, composed_choi

machine.finalize()
