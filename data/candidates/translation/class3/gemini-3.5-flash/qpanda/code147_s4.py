# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import *

def mcy(qc):
    machine = get_current_machine()
    q = [machine.get_qubit_by_phy_addr(i) for i in range(5)]
    gate = Y(q[4]).control([q[0], q[1], q[2], q[3]])
    qc << gate
    return qc
