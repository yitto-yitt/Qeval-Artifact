# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init()
q = machine.qAlloc_many(1)

def circuit():
    vqc = VariationalQuantumCircuit()
    vqc.insert(H(q[0]))
    theta = vqc.insert_parameter("th")
    vqc.insert(RZ(q[0], theta))
    return vqc

machine.finalize()
