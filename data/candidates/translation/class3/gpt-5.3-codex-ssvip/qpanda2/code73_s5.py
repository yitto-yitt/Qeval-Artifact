# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_q = machine.qAlloc_many(64)
_c = machine.cAlloc_many(64)

def x_measurement(circuit, qubit, clbit):
    circuit.insert(H(_q[qubit]))
    circuit.insert(Measure(_q[qubit], _c[clbit]))
    return circuit

machine.finalize()
