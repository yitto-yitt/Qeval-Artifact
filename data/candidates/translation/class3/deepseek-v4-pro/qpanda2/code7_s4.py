# EVAL_META: task_id=7, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = var("theta", 0.0)
    vqc = VariationalQuantumCircuit()
    vqc.insert(RX(q[0], theta))
    return vqc

machine.finalize()
