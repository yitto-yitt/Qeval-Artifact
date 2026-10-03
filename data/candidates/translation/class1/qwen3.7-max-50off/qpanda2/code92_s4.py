# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np

def calculate_stabilizer_state_info():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    qvm.run(prog)
    state = qvm.get_qstate()
    
    probs = np.abs(state)**2
    
    prob_dict = {}
    for i in range(4):
        bitstring = format(i, '02b')
        prob_dict[bitstring] = float(probs[i])
        
    return prob_dict
