# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    prog << pq.CSWAP(q[0], q[1], q[3])
    prog << pq.CNOT(q[2], q[3])
    machine.directly_run(prog)
    return prog

machine.finalize()
