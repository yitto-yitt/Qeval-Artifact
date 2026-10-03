# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
_qbits = machine.qAlloc_many(32)
_cbits = machine.cAlloc_many(32)


def x_measurement(circuit, qubit, clbit):
    if isinstance(qubit, int):
        qubit = _qbits[qubit]
    if isinstance(clbit, int):
        clbit = _cbits[clbit]
    circuit << H(qubit)
    circuit << Measure(qubit, clbit)


atexit.register(machine.finalize)
