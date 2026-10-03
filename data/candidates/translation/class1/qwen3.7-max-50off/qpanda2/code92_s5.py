# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    
    try:
        prob_dict = qvm.get_prob_dict(prog, q)
        res = {}
        for k, v in prob_dict.items():
            if v > 1e-7:
                if isinstance(k, int):
                    res[f"{k:02b}"] = v
                else:
                    res[str(k)] = v
        return res
    except Exception:
        probs = qvm.get_prob_list(prog, q)
        res = {}
        for i, p in enumerate(probs):
            if p > 1e-7:
                res[f"{i:02b}"] = p
        return res
