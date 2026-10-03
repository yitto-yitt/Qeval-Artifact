# EVAL_META: task_id=90, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

atexit.register(machine.finalize)

def create_custom_controlled():
    qc = pq.QCircuit()
    qc.insert(pq.X(q[1]).control([q[0], q[3]]))
    qc.insert(pq.H(q[2]).control([q[0], q[3]]))
    return qc
