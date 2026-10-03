# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
import pyqpanda as pq


def w_state():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)

    circuit = pq.QCircuit()
    circuit << pq.RY(q[0], 2 * arccos(1 / sqrt(3)))
    circuit << pq.CH(q[0], q[1])
    circuit << pq.CNOT(q[1], q[2])
    circuit << pq.CNOT(q[0], q[1])
    circuit << pq.X(q[0])

    prog = pq.QProg()
    prog << circuit
    for i in range(3):
        prog << pq.measure(q[i], c[i])

    return prog
