# EVAL_META: task_id=73, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_q = machine.qAlloc_many(1)
_c = machine.cAlloc_many(1)
atexit.register(machine.finalize)

def x_measurement(circuit, qubit, clbit):
    circuit.insert(H(qubit))
    circuit.insert(Measure(qubit, clbit))
