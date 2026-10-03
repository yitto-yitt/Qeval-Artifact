# EVAL_META: task_id=57, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_swap_gate():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.CNOT(q[1], q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    return prog
