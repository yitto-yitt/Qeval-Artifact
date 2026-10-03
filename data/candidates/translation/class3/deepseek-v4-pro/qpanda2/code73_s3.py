# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_q = machine.qAlloc_many(1)
_c = machine.cAlloc_many(1)

def x_measurement(circuit, qubit, clbit):
    circuit << H(qubit)
    circuit << Measure(qubit, clbit)

machine.finalize()
