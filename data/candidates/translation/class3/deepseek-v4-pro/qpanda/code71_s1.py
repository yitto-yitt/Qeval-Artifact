# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3 import *

def create_quantum_circuit_based_h0_csx01_h1():
    machine = CPUQVM()
    machine.init()
    q = machine.qAlloc_many(3)
    qc = QCircuit()
    qc << H(q[0]) << SX(q[1]).control(q[0]) << H(q[1])
    return qc
