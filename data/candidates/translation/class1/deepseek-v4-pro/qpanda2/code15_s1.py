# EVAL_META: task_id=15, framework=qpanda2, class=1
import pyqpanda as pq

def noisy_bell():
    pq.init(pq.QMachineType.CPU)
    q = pq.qAlloc_many(2)
    c = pq.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    shots = 1000
    counts = pq.run_with_configuration(prog, c, shots)
    total = shots
    distribution = {key: value / total for key, value in counts.items()}
    pq.destroy()
    return distribution
