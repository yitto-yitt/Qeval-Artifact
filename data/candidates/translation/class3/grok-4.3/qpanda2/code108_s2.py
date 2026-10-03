# EVAL_META: task_id=108, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def initialize_adjoint_and_compose(data1, data2):
    prog = QProg()
    prog.insert(CZ(q[0], q[1]))
    result = machine.directly_run(prog)
    choi1 = data1
    adjoint_choi1 = machine.get_qstate()
    composed_choi = data2
    return choi1, adjoint_choi1, composed_choi

machine.finalize()
