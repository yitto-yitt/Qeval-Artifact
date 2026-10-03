# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, init_state

def init_random_3qubit(desired_vector):
    qvm = CPUQVM()
    qvm.init_qvm()
    qvec = qvm.qAlloc_many(3)
    
    prog = QProg()
    prog << init_state(qvec, desired_vector)
    
    prob_dict = qvm.prob_run_dict(prog, qvec)
    
    result = {k: v for k, v in prob_dict.items() if v > 1e-9}
    total = sum(result.values())
    if total > 0:
        result = {k: v / total for k, v in result.items()}
        
    return result
