# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, StateVector


def create_bell_statevector():
    qvm = CPUQVM()
    qvm.init_qvm()
    prog = QProg()
    prog << H(0) << CNOT(0, 1)
    qvm.run(prog, 1)
    state = qvm.get_qstate()
    return StateVector(state)
