# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import *

def get_statevector(circuit):
    machine = CPUQVM()
    machine.init_qvm()
    try:
        qnum = circuit.get_qubit_num()
    except Exception:
        qnum = 0
    if qnum > 0:
        machine.qAlloc_many(qnum)
    machine.directly_run(circuit)
    state = machine.get_qstate()
    machine.finalize()
    return state
