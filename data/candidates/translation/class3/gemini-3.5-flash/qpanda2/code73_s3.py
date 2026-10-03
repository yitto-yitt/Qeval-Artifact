# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
c = machine.cAlloc_many(4)

def x_measurement(circuit, qubit, clbit):
    circuit << H(qubit) << Measure(qubit, clbit)
    return circuit

machine.finalize()
