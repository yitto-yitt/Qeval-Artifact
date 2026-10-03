# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    qc = QCircuit()
    qc << X1(q[3]).control([q[0], q[1], q[2]])
    return qc

machine.finalize()
