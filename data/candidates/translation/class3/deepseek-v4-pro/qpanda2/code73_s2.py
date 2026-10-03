# EVAL_META: task_id=73, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(16)
c = machine.cAlloc_many(16)

def x_measurement(circuit, qubit, clbit):
    qbit = q[qubit] if isinstance(qubit, int) else qubit
    cbit = c[clbit] if isinstance(clbit, int) else clbit
    circuit << H(qbit) << measure(qbit, cbit)

atexit.register(machine.finalize)
