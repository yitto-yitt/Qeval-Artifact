# EVAL_META: task_id=40, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def init_random_3qubit(desired_vector):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = QProg()
    prog << init_state(qubits, desired_vector)
    
    for i in range(3):
        prog << Measure(qubits[i], cbits[i])
        
    shots = 10000
    result = qvm.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(result.values())
    probs = {}
    for key, val in result.items():
        probs[key[::-1]] = val / total
        
    return probs
