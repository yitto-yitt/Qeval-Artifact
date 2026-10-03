# EVAL_META: task_id=89, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_controlled_hgate():
    cir = pq.QCircuit()
    cir << pq.RY(q[2], -np.pi/4)
    cir << pq.Toffoli(q[0], q[1], q[2])
    cir << pq.RY(q[2], np.pi/4)
    return cir

machine.finalize()
