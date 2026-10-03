# EVAL_META: task_id=105, framework=qpanda, class=3
import pyqpanda3.core as pq

_machine = pq.CPUQVM()
_machine.init_qvm()
_q = _machine.qAlloc_many(2)


def initialize_cnot_dihedral():
    prog = pq.QProg()
    prog << pq.CNOT(_q[0], _q[1]) << pq.T(_q[0])
    return prog
