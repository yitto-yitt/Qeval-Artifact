# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def init_random_3qubit(desired_vector):
    prog = QProg()
    qubits = qAlloc(3)
    cbits = cAlloc(3)
    
    prog << amplitude_encode(desired_vector, qubits)
    prog << measure(qubits, cbits)
    
    qvm = CPUQVM()
    qvm.init_qvm()
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(result.values())
    prob_dist = {}
    for key, count in result.items():
        bitstring = format(key, '03b')[::-1]
        prob_dist[bitstring] = count / total
    return prob_dist
