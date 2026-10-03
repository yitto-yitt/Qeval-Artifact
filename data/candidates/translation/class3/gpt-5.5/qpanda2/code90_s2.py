# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
atexit.register(machine.finalize)

def create_custom_controlled():
    prog = QProg()
    controls = [q[0], q[3]]
    custom = QCircuit()
    custom.insert(X(q[1]).control(controls))
    custom.insert(H(q[2]).control(controls))
    prog.insert(custom)
    return prog
