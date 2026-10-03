# EVAL_META: task_id=60, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_cy_gate():
    prog = pq.QProg()
    prog << pq.Sdag(q[1]) << pq.CNOT(q[0], q[1]) << pq.S(q[1])
    machine.directly_run(prog)
    machine.finalize()
    return prog
