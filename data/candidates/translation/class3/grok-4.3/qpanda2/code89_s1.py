# EVAL_META: task_id=89, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_controlled_hgate():
    qc = pq.QCircuit()
    c3h_gate = pq.H(q[2]).control([q[0], q[1]])
    qc << c3h_gate
    return qc

machine.finalize()
