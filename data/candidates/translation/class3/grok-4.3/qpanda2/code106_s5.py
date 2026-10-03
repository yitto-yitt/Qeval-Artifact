# EVAL_META: task_id=106, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = qAlloc_many(2)
def compose_cnot_dihedral():
    prog = QProg()
    prog << CNOT(q[0], q[1]) << T(q[0]) << X(q[1]) << CNOT(q[0], q[1]) << T(q[0])
    machine.directly_run(prog)
    result = machine.get_qstate()
    return result
machine.finalize()
