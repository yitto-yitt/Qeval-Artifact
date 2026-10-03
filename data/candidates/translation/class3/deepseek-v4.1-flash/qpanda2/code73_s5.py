# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
clbits = machine.cAlloc_many(10)

def x_measurement(circuit, qubit, clbit):
    circuit << H(qubit) << Measure(qubit, clbit)
    return circuit

machine.finalize()
