# EVAL_META: task_id=2, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_bell_statevector():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    machine.directly_run(prog)
    state = machine.get_qstate()
    machine.finalize()
    return state
