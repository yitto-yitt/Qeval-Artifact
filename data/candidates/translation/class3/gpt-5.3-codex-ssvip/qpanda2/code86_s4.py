# EVAL_META: task_id=86, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    prog_full = pq.QProg()
    prog_full.insert(pq.H(q[0]))
    prog_full.insert(pq.CNOT(q[0], q[1]))
    prog_full.insert(pq.CNOT(q[1], q[2]))
    prog_full.insert(pq.CNOT(q[2], q[3]))
    prog_full.insert(pq.CNOT(q[3], q[4]))

    prog_limited = pq.QProg()
    prog_limited.insert(pq.H(q[0]))
    prog_limited.insert(pq.CNOT(q[0], q[1]))
    prog_limited.insert(pq.CNOT(q[1], q[2]))
    prog_limited.insert(pq.CNOT(q[2], q[3]))
    prog_limited.insert(pq.CNOT(q[3], q[4]))

    machine.directly_run(prog_full)
    machine.directly_run(prog_limited)

    return prog_full, prog_limited

machine.finalize()
