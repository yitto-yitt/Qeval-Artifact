# EVAL_META: task_id=6, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_state_prep(num_qubits):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    if num_qubits > 0:
        prog << pq.X(qubits[0])
    return prog
