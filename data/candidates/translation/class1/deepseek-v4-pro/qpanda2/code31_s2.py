# EVAL_META: task_id=31, framework=qpanda2, class=1
import pyqpanda as pq

def sampler_qiskit():
    qvm = pq.CPUQVM()
    qvm.init()
    qvm.set_random_seed(42)

    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) \
         << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])

    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)
    qvm.finalize()

    return {bitstring: count / shots for bitstring, count in counts.items()}
