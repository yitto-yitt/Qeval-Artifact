# EVAL_META: task_id=58, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_ch_gate():
    circuit = QCircuit()
    circuit << RY(q[1], pi/4) << CNOT(q[0], q[1]) << RY(q[1], -pi/4)
    return circuit

machine.finalize()
