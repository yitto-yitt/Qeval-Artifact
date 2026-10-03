# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(16)
c = machine.cAlloc_many(16)

def x_measurement(circuit, qubit, clbit):
    if isinstance(qubit, int):
        qubit = q[qubit]
    if isinstance(clbit, int):
        clbit = c[clbit]
    circuit << H(qubit) << Measure(qubit, clbit)

if __name__ == '__main__':
    machine.finalize()
