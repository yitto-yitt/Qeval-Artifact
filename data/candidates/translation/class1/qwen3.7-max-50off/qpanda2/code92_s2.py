# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    
    prob_dict = qvm.get_prob_dict(prog, q)
    
    qvm.finalize()
    return prob_dict
