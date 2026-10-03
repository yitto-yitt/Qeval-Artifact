# EVAL_META: task_id=147, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, Y

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def mcy(qc):
    qc << Y(qubits[4]).control(qubits[:4])
    return qc


atexit.register(machine.finalize)
