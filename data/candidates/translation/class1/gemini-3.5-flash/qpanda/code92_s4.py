# EVAL_META: task_id=92, framework=qpanda, class=1
import pyqpanda3.core as pq

def calculate_stabilizer_state_info():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    
    prob_dict = machine.prob_run_dict(prog, q, -1)
    machine.finalize()
    
    # Filter out zero probabilities to match Qiskit's StabilizerState.probabilities_dict()
    non_zero_probs = {k: v for k, v in prob_dict.items() if v > 1e-9}
    return non_zero_probs
