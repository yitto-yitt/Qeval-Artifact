# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
cbits = machine.cAlloc_many(20)

def x_measurement(circuit, qubit, clbit):
    circuit << H(qubits[qubit])
    circuit << measure(qubits[qubit], cbits[clbit])

machine.finalize()
