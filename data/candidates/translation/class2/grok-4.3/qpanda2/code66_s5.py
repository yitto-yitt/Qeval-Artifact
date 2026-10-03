# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
import pyqpanda as pq


def w_state():
    machine = pq.CPUQVM()
    machine.initQVM()
    q = machine.qAllocMany(3)
    c = machine.cAllocMany(3)
    prog = pq.QProg()
    circuit = pq.QCircuit()
    circuit.insert(pq.RY(q[0], 2 * arccos(1 / sqrt(3))))
    circuit.insert(pq.H(q[1]).control([q[0]]))
    circuit.insert(pq.CNOT(q[1], q[2]))
    circuit.insert(pq.CNOT(q[0], q[1]))
    circuit.insert(pq.X(q[0]))
    prog.insert(circuit)
    prog.insert(pq.measure_all(q, c))
    return prog
