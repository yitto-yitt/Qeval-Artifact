# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(16)
_cbits = machine.cAlloc_many(16)

def x_measurement(circuit, qubit, clbit):
    circuit << H(qubit)
    circuit << Measure(qubit, clbit)

machine.finalize()
