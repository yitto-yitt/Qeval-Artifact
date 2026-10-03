# EVAL_META: task_id=66, framework=qpanda, class=2
import pyqpanda3.core as pq
from numpy import arccos, sqrt

def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    prog = pq.QProg()
    circuit = pq.QCircuit()
    theta = 2 * arccos(1 / sqrt(3))
    circuit << pq.RY(q[0], theta)
    circuit << pq.H(q[1]).control(q[0])
    circuit << pq.CNOT(q[1], q[2])
    circuit << pq.CNOT(q[0], q[1])
    circuit << pq.X(q[0])
    prog << circuit
    prog << pq.measure_all(q, c)
    return prog
