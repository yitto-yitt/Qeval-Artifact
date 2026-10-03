# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import *

def simple_elitzur_vaidman():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << CNOT(q[0], q[1])
    circuit << H(q[0])
    return circuit
