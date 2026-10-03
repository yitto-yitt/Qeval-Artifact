# EVAL_META: task_id=10, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
cbits = machine.cAlloc_many(2)

def create_operator():
    prog = QProg()
    prog.insert(X(qubits[0]))
    prog.insert(X(qubits[1]))
    return prog

def _finalize_machine():
    machine.finalize()

atexit.register(_finalize_machine)
