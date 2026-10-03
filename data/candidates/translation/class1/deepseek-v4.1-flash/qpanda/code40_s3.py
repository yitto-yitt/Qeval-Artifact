# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, amplitude_encode, Measure

def init_random_3qubit(desired_vector):
    vec = np.array(desired_vector, dtype=complex)
    vec = vec / np.linalg.norm(vec)
    vec_list = [complex(x) for x in vec]
    
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = QProg()
    prog << amplitude_encode(qubits, vec_list)
    for i in range(3):
        prog << Measure(qubits[i], cbits[i])
    
    result = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
