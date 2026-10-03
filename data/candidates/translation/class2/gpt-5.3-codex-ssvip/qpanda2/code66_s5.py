# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
import pyqpanda as pq


def w_state():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog.insert(pq.RY(q[0], 2 * arccos(1 / sqrt(3))))
    prog.insert(pq.CH(q[0], q[1]))
    prog.insert(pq.CNOT(q[1], q[2]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.X(q[0]))
    prog.insert(pq.measure_all(q, c))

    return prog
