# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)

    prog = pq.QProg()
    prog << pq.X(qubits[1])

    return prog
