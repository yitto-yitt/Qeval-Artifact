# EVAL_META: task_id=108, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
qubits = machine.qAlloc_many(4)

def initialize_adjoint_and_compose(data1, data2):
    # Convert numpy arrays to the format expected by pyqpanda if needed
    choi1 = pq.Choi(data1)
    choi2 = pq.Choi(data2)
    
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    
    return choi1, adjoint_choi1, composed_choi

machine.finalize()
