# EVAL_META: task_id=2, framework=qpanda, class=2
from math import sqrt
from pyqpanda3.core import QProg, H, CNOT, QMachineType, QMachineFactory, StateVector, init, destroy

def create_bell_statevector():
    init(QMachineType.CPU)
    machine = QMachineFactory.create(QMachineType.CPU)
    machine.init()
    q = machine.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    machine.execute(prog)
    state_vec = machine.get_qstate()
    sv = StateVector(state_vec)
    machine.free()
    destroy()
    return sv
