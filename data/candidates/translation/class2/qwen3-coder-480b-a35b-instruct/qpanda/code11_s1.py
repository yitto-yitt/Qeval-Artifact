# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import *

def get_statevector(circuit):
    machine = CPUQVM()
    machine.init_qvm()
    prog = QProg()
    prog.insert(circuit)
    result = machine.run_with_configuration(prog, [], 0)
    sv = machine.get_qstate()
    machine.finalize()
    return sv
