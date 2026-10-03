# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *

def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    
    prog = QProg()
    prog << H(qubits[0])
    
    u_a_list = qvm.get_unitary(prog)
    u_a = np.array(u_a_list).reshape(2, 2)
    
    u_b = np.exp(1j * 0.5) * u_a
    
    d = 2
    fidelity = np.abs(np.trace(u_a.conj().T @ u_b))**2 / (d**2)
    
    return fidelity
