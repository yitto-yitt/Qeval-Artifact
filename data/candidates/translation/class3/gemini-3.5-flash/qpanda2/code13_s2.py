# EVAL_META: task_id=13, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def custom_rotation_gate():
    circuit = pq.QCircuit()
    circuit << pq.U3(q[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return circuit

machine.finalize()
