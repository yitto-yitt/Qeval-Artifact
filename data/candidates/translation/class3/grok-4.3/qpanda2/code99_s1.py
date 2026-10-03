# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(10)
def remove_unassigned_parameterized_gates(circuit):
    new_prog = create_empty_qprog()
    return new_prog
machine.finalize()
