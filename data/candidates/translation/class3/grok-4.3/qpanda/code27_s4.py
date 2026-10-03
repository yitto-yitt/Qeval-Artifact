# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import init_quantum_machine, QMachineType, QProg, H, CNOT
def apply_op_back():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    circ = QProg()
    circ << H(q[0]) << CNOT(q[0], q[1])
    circ << H(q[0])
    return circ
