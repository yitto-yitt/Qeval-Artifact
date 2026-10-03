# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prob_dict = machine.prob_run_dict(prog, q)
    return prob_dict
