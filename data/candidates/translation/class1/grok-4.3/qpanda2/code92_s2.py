# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq
import builtins
def calculate_stabilizer_state_info():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prog << pq.measure_all(q, c)
    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    probabilities_dict = {k: v / total for k, v in counts.items()}
    return probabilities_dict
