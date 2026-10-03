# EVAL_META: task_id=49, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def simple_elitzur_vaidman():
    circuit = QProg()
    circuit << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    return circuit

machine.finalize()
