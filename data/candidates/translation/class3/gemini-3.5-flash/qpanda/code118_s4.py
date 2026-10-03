# EVAL_META: task_id=118, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_c3sx_circuit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(4)
    prog = pq.QProg()
    gate = pq.SX(q[3]).control([q[0], q[1], q[2]])
    prog.insert(gate)
    return prog
