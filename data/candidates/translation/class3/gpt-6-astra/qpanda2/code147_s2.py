# EVAL_META: task_id=147, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QProg, Y

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)
atexit.register(machine.finalize)


def mcy(qc):
    qc << Y(qubits[4]).control(qubits[:4])
    program = QProg()
    program << qc
    machine.directly_run(program)
    return qc
