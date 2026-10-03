# EVAL_META: task_id=86, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.CNOT(q[1], q[2]))
    prog.insert(pq.CNOT(q[2], q[3]))
    prog.insert(pq.CNOT(q[3], q[4]))

    full_block = prog
    limited_block = prog

    return full_block, limited_block

machine.finalize()
