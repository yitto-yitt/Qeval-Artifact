# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import CPUQVM

def get_statevector(circuit):
    machine = CPUQVM()
    machine.initQVM()
    machine.directly_run(circuit)
    sv = machine.getQState()
    return sv
