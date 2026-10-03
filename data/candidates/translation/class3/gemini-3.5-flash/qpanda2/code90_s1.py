# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    cir = pq.QCircuit()
    cir << pq.X(q[1]) << pq.H(q[2])
    controlled_cir = cir.control([q[0], q[3]])
    prog = pq.QProg()
    prog << controlled_cir
    return prog

machine.finalize()
