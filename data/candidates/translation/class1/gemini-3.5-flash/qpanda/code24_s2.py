# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *

def dj_algorithm(oracle):
    # Get the qubits from the oracle
    qubits = get_all_used_qubits(oracle)
    qubits.sort(key=lambda q: q.get_phy_addr())
    n = len(qubits)
    
    # Initialize machine
    machine = CPUQVM()
    machine.init_qvm()
    
    # Allocate qubits in this machine
    q = machine.allocate_qubits(n)
    
    # Build program
    prog = QProg()
    prog << X(q[-1])
    for i in range(n):
        prog << H(q[i])
    
    prog << oracle
    
    for i in range(n):
        prog << H(q[i])
        
    # Get probabilities for the first n-1 qubits
    q_list = q[:n-1]
    
    # Run probability
    prob_dict = machine.prob_run_dict(prog, q_list)
    
    # Reverse keys to match Qiskit's LSB-first endianness
    return {k[::-1]: v for k, v in prob_dict.items()}
