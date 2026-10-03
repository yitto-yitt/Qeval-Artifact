# EVAL_META: task_id=26, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QProg, H, CNOT, Measure

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
c = machine.cAlloc_many(3)
atexit.register(machine.finalize)


def bell_dag():
    prog = QProg()
    prog.insert(H(q[0]))
    prog.insert(CNOT(q[0], q[1]))
    prog.insert(Measure(q[0], c[0]))
    return prog
