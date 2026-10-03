# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    custom = pq.QCircuit()
    custom << pq.X(q[1])
    custom << pq.H(q[2])
    
    controlled_custom = custom.control([q[0], q[3]])
    
    prog = pq.QProg()
    prog << controlled_custom
    return prog

machine.finalize()
