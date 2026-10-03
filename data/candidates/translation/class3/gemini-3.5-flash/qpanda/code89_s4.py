# EVAL_META: task_id=89, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_controlled_hgate():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    prog = pq.QProg()
    gate = pq.H(q[2]).control(q[0:2])
    prog.insert(gate)
    return prog
