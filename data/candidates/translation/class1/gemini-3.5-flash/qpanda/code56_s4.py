# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3.core as pq

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(8)
    prog = pq.QProg()
    
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7-i] == "0":
            prog << pq.X(q[i])
            
    q_list = [q[i] for i in range(7, -1, -1)]
    result = machine.prob_run_dict(prog, q_list, -1)
    
    return {k: v for k, v in result.items() if v > 0}
