# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    pq.init(pq.QMachineType.CPU)
    q = pq.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    probs = pq.prob_run_dict(prog, q)
    pq.finalize()
    return {k: round(v, 12) for k, v in probs.items() if round(v, 12) > 0}
