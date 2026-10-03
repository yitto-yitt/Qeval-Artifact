# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    prog << pq.X(q[0])
    return prog
