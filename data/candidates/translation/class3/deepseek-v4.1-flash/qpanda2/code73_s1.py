# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(10)
cbits = cAlloc_many(10)

def x_measurement(circuit, qubit, clbit):
    circuit << H(qubits[qubit])
    circuit << measure(qubits[qubit], cbits[clbit])

machine.finalize()
